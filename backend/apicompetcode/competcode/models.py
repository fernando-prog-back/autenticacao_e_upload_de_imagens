from competcode import db
from enum import Enum


# ==============================
# ENUM - STATUS DA SUBMISSÃO
# ==============================
class StatusSubmissao(Enum):
    PENDENTE = 'Pending'
    ACEITO = 'Accepted'
    RESPOSTA_ERRADA = 'Wrong Answer'
    TEMPO_EXCEDIDO = 'Time Limit Exceeded'
    ERRO_EXECUCAO = 'Runtime Error'
    ERRO_COMPILACAO = 'Compilation Error'


# ==============================
# TABELA: USER
# ==============================
class User(db.Model): 
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)  # corrigido tamanho
    ranking = db.Column(db.String(5), default='E')
    image = db.Column(db.String(50), default='default.jpeg')
    score = db.Column(db.Float,nullable=False, default=0)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    
    role = db.Column(db.String(20), default="user")

    # RELAÇÃO: User -> Submissao (1:N)
    submissoes = db.relationship(
        "Submissao",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )


# ==============================
# TABELA: PROBLEMA
# ==============================
class Problema(db.Model):
    __tablename__ = 'problema'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)

    tempo_limite = db.Column(db.Integer)   # corrigido (não é PK)
    memoria_limite = db.Column(db.Integer) # corrigido (não é PK)

    dificuldade = db.Column(db.String(20))
    criado_em = db.Column(db.DateTime, server_default=db.func.now())

    # RELAÇÃO: Problema -> Teste (1:N)
    testes = db.relationship(
        'Teste',
        back_populates='problema',
        cascade="all, delete-orphan",
        lazy=True
    )

    # RELAÇÃO: Problema -> Submissao (1:N)
    submissoes = db.relationship(
        'Submissao',
        back_populates='problema',
        cascade="all, delete-orphan",
        lazy=True
    )


# ==============================
# TABELA: TESTE
# ==============================
class Teste(db.Model):
    __tablename__ = 'teste'

    id = db.Column(db.Integer, primary_key=True)

    problema_id = db.Column(
        db.Integer,
        db.ForeignKey('problema.id', ondelete='CASCADE'),
        nullable=False
    )

    entrada = db.Column(db.Text, nullable=False)
    saida_esperada = db.Column(db.Text, nullable=False)

    # RELAÇÃO: Teste -> Problema (N:1)
    problema = db.relationship(
        'Problema',
        back_populates='testes'
    )

# ==============================
# TABELA: SUBMISSAO
# ==============================
class Submissao(db.Model):
    __tablename__ = 'submissao'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    problema_id = db.Column(
        db.Integer,
        db.ForeignKey('problema.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    linguagem = db.Column(db.String(30), nullable=False)
    codigo = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.Enum(StatusSubmissao),
        default=StatusSubmissao.PENDENTE,
        nullable=False,
        index=True
    )
    tempo_execucao = db.Column(db.Integer)
    memoria_usada = db.Column(db.Integer)
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    # RELAÇÃO: Submissao -> User (N:1)
    user = db.relationship(
        'User',
        back_populates='submissoes'
    )
    # RELAÇÃO: Submissao -> Problema (N:1)
    problema = db.relationship(
        'Problema',
        back_populates='submissoes'
    )
    # RELAÇÃO: Submissao -> Resultado (1:N)
    resultados = db.relationship(
        'Resultado',
        back_populates='submissao',
        cascade="all, delete-orphan",
        lazy=True
    )

# ==============================
# TABELA: RESULTADO
# ==============================
class Resultado(db.Model):
    __tablename__ = 'resultado'

    id = db.Column(db.Integer, primary_key=True)

    submissao_id = db.Column(
        db.Integer,
        db.ForeignKey('submissao.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )

    teste_id = db.Column(
        db.Integer,
        db.ForeignKey('teste.id', ondelete='CASCADE'),
        nullable=False
    )

    status = db.Column(
        db.Enum(StatusSubmissao),
        nullable=False
    )

    tempo = db.Column(db.Integer)

    # RELAÇÃO: Resultado -> Submissao (N:1)
    submissao = db.relationship(
        'Submissao',
        back_populates='resultados'
    )