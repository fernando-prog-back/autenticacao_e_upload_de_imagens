from app import app, db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# ==============================
# TABELA: USER
# ==============================
class User(db.Model,UserMixin): 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(120), nullable=False, unique=True)

    password = db.Column(db.String(200), nullable=False)  # corrigido tamanho

    image = db.Column(db.String(50), default='default.jpeg')

    criado_em = db.Column(db.DateTime, server_default=db.func.now())


    # RELAÇÃO: User -> Submissao (1:N)
    books = db.relationship(
        "Book",
        backref="user",
        cascade="all, delete-orphan",
        lazy=True
    )


# ==============================
# TABELA: PROBLEMA
# ==============================
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)

    disciplina = db.Column(db.String(200), nullable=False)
    curso = db.Column(db.Text, nullable=False)
    classe = db.Column(db.Text, nullable=False)
    Ano_lectivo = db.Column(db.Text, nullable=False)

    criado_em = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    capitulo = db.relationship(
        'Capitulo',
        backref='book',
        cascade="all, delete-orphan",
        passive_deletes=True
    )


# ==============================
# TABELA: TESTE
# ==============================
class Capitulo(db.Model):
    __tablename__ = 'capitulos'

    id = db.Column(db.Integer, primary_key=True)

    tema = db.Column(db.Text, nullable=False)

    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', ondelete='CASCADE'),
        nullable=False
    )

    materias = db.relationship(
        'Materia',
        backref='capitulo',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

# ==============================
# TABELA: SUBMISSAO
# ==============================
class Materia(db.Model):
    __tablename__ = 'materias'
    id = db.Column(db.Integer, primary_key=True)

    Sumario = db.Column(db.Text, nullable=False)

    capitulo_id = db.Column(
        db.Integer,
        db.ForeignKey('capitulos.id', ondelete='CASCADE'),
        nullable=False
    )
    criado_em = db.Column(db.DateTime, server_default=db.func.now())
    
    paginas = db.relationship(
        'Pagina',
        backref='materia',
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class Pagina(db.Model):
    __tablename__ = 'paginas'

    id = db.Column(db.Integer, primary_key=True)

    conteudo = db.Column(db.Text, nullable=False)

    materia_id = db.Column(
        db.Integer,
        db.ForeignKey('materias.id', ondelete='CASCADE'),
        nullable=False
    )

with app.app_context():
    db.create_all()