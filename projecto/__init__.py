from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config

# Inicialização do Flask e extensões
app = Flask(__name__)
app.config.from_object(Config)


# Configurações do SQLAlchemy, Migrate e Bcrypt
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


# Importar rotas e modelos
from projecto.views import homepage
from projecto.models import Usuario, Admin, Arquivo