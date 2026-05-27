from celery import Celery
import requests
import time
import hashlib
import redis
from concurrent.futures import ThreadPoolExecutor

# 🔥 IMPORTANTE (FLASK APP)
from competcode import app, db
from competcode.models import Submissao, Teste, Resultado, StatusSubmissao, User

# =========================
# CELERY + REDIS
# =========================

celery = Celery(
    "judge",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery.conf.update(
    task_track_started=True,
    worker_concurrency=10  # 🔥 máximo 10 execuções
)

# Redis extra (cache + rate limit)
r = redis.Redis(host="localhost", port=6379, db=2)


# =========================
# WEBSOCKET (OPCIONAL)
# =========================

try:
    from flask_socketio import SocketIO
    socketio = SocketIO(message_queue="redis://localhost:6379/0")
except:
    socketio = None


def emit(event, data):
    if socketio:
        socketio.emit(event, data)


# =========================
# LANGUAGE MAP
# =========================

LANGUAGE_MAP = {
    "python": 71,
    "javascript": 63,
    "java": 62,
    "c": 50,
    "cpp": 54,
    "csharp": 51,
    "typescript": 74,
    "go": 60,
    "rust": 73,
    "kotlin": 78
}


# =========================
# RATE LIMIT
# =========================

def check_rate_limit(user_id):
    key = f"rate:{user_id}"
    count = r.incr(key)

    if count == 1:
        r.expire(key, 60)

    return count <= 10


# =========================
# CACHE
# =========================

def hash_submission(code, problem_id):
    return hashlib.md5(f"{code}:{problem_id}".encode()).hexdigest()


def get_cache(key):
    data = r.get(key)
    return eval(data) if data else None


def set_cache(key, value):
    r.set(key, str(value), ex=3600)


# =========================
# JUDGE0 SERVICE
# =========================

class Judge0Service:

    BASE_URL = "https://judge0-ce.p.rapidapi.com"

    @staticmethod
    def run(code, language_id, stdin):

        response = requests.post(
            f"{Judge0Service.BASE_URL}/submissions",
            json={
                "source_code": code,
                "language_id": language_id,
                "stdin": stdin
            },
            headers={"Content-Type": "application/json"}
        )

        token = response.json()["token"]

        result = None

        for _ in range(20):
            result = requests.get(
                f"{Judge0Service.BASE_URL}/submissions/{token}"
            ).json()

            if result["status"]["id"] not in [1, 2]:
                break

            time.sleep(0.8)

        return result


# =========================
# CELERY TASK
# =========================

@celery.task(bind=True)
def run_submission(self, submission_id):

    # 🔥 CORREÇÃO CRÍTICA AQUI
    with app.app_context():

        submission = Submissao.query.get(submission_id)

        if not submission:
            return

        print(f"[Judge] Processando submissão {submission_id}")

        # =========================
        # RATE LIMIT
        # =========================
        if not check_rate_limit(submission.usuario_id):
            submission.status = StatusSubmissao.ERRO_EXECUCAO
            db.session.commit()
            return {"error": "rate limit excedido"}

        # =========================
        # CACHE
        # =========================
        cache_key = hash_submission(
            submission.codigo,
            submission.problema_id
        )

        cached = get_cache(cache_key)

        if cached:
            submission.status = StatusSubmissao.ACEITO
            db.session.commit()
            return cached

        try:
            # =========================
            # LANGUAGE
            # =========================
            language_id = LANGUAGE_MAP.get(submission.linguagem)

            if not language_id:
                submission.status = StatusSubmissao.ERRO_COMPILACAO
                db.session.commit()
                return

            submission.status = StatusSubmissao.PENDENTE
            db.session.commit()

            # =========================
            # BUSCAR TESTES
            # =========================
            testes = Teste.query.filter_by(
                problema_id=submission.problema_id
            ).all()

            todos_ok = True
            max_time = 0
            max_memory = 0

            # =========================
            # EXECUÇÃO PARALELA
            # =========================
            def run_test(teste):
                result = Judge0Service.run(
                    submission.codigo,
                    language_id,
                    teste.entrada
                )
                return teste, result

            with ThreadPoolExecutor(max_workers=3) as executor:
                responses = list(executor.map(run_test, testes))

            # =========================
            # PROCESSAMENTO
            # =========================
            for teste, result in responses:

                stdout = (result.get("stdout") or "").strip()
                expected = (teste.saida_esperada or "").strip()

                status_id = result["status"]["id"]

                time_exec = float(result.get("time") or 0)
                memory_exec = float(result.get("memory") or 0)

                max_time = max(max_time, time_exec)
                max_memory = max(max_memory, memory_exec)

                emit("judge_update", {
                    "submission_id": submission.id,
                    "teste_id": teste.id,
                    "status": result["status"]["description"]
                })

                # Compilation Error
                if status_id == 6:
                    submission.status = StatusSubmissao.ERRO_COMPILACAO
                    todos_ok = False
                    break

                # Runtime Error
                if status_id == 5:
                    submission.status = StatusSubmissao.ERRO_EXECUCAO
                    todos_ok = False
                    break

                # Wrong Answer
                if stdout != expected:
                    submission.status = StatusSubmissao.RESPOSTA_ERRADA
                    todos_ok = False
                    break

                # Accepted
                db.session.add(Resultado(
                    submissao_id=submission.id,
                    teste_id=teste.id,
                    status=StatusSubmissao.ACEITO,
                    tempo=time_exec
                ))

            # =========================
            # FINAL
            # =========================
            if todos_ok:
                submission.status = StatusSubmissao.ACEITO

                user = User.query.get(submission.usuario_id)
                user.score += 10

            submission.tempo_execucao = int(max_time)
            submission.memoria_usada = int(max_memory)

            db.session.commit()

            # =========================
            # CACHE SAVE
            # =========================
            set_cache(cache_key, {
                "submission_id": submission.id,
                "status": submission.status.value
            })

            # =========================
            # ANTI-PLÁGIO (SIMPLES)
            # =========================
            similar = Submissao.query.filter_by(
                problema_id=submission.problema_id
            ).all()

            for s in similar:
                if s.id != submission.id:
                    similarity = len(set(s.codigo.split()) & set(submission.codigo.split()))
                    if similarity > 20:
                        print("⚠️ POSSÍVEL PLÁGIO DETECTADO")

            return {
                "submission_id": submission.id,
                "status": submission.status.value
            }

        except Exception as e:
            submission.status = StatusSubmissao.ERRO_EXECUCAO
            db.session.commit()

            raise self.retry(exc=e, countdown=5, max_retries=3)