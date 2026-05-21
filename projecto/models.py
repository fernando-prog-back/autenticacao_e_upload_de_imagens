from projecto import db, app


# =========================
# USER TABLE
# =========================
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # relação com arquivos
    arquivos = db.relationship(
        "Arquivo",
        backref="usuario",
        cascade="all, delete-orphan",
        lazy=True
    )


# =========================
# ADMIN TABLE
# =========================
class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# =========================
# FILE TABLE
# =========================
class Arquivo(db.Model):
    __tablename__ = "arquivos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50))
    caminho = db.Column(db.String(300), nullable=False)

    # FK -> usuário dono do arquivo
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id', ondelete="CASCADE"),
        nullable=False
    )
