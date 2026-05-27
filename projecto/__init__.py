from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config

# caminho para uploads
UPLOAD_FOLDER = 'projecto/static/upload'

# Inicialização do Flask e extensões
app = Flask(__name__)
CORS(app)  # Habilitar CORS para permitir requisições de diferentes origens
app.config.from_object(Config)


# Configurações do SQLAlchemy, Migrate e Bcrypt
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


# Importar rotas e modelos
from projecto.views import homepage
from projecto.models import Usuario, Admin, Arquivo