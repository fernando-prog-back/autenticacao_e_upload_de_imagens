from app import create_app


@celery.task
def dizer_ola():
    print("🔥 Olá Mundo vindo do Celery!")
    return "ok"