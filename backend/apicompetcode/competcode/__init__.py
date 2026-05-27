from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)

#----------onde sera feito o upload das imagens-----------
UPLOAD_FOLDER = 'apicompetcode/competcode/static/uploads'


app.config.from_object(Config)
app.config["JSON_AS_ASCII"]=False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# tempo do token normal
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hora

# tempo do refresh (lembrar login)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 60 * 60 * 24 * 30  # 30 dias




CORS(app)

db = SQLAlchemy(app)
migrate=Migrate(app, db)
bcrypt=Bcrypt(app)
jwt = JWTManager(app)


from competcode.contollers import home
from competcode.models import Problema,Resultado, Submissao, Teste, User