from app.models import User
from app import bcrypt
import re

# validar email

def validar_email(email):
    
    padrao = r'^[a-zA-Z0-9]+@(gmail\.com|hotmail\.com)$'

    if not isinstance(email,str) or not re.match(padrao,email):
        raise ValueError('E-mail Inválido  dsdfs')

    if User.query.filter_by(email=email).first():
        raise ValueError('E-mail Inválido')
    
    return email.lower()

# validar senha
def validar_senha(senha):
    
    padrao = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,16}$'

    if len(senha) < 8:
        raise ValueError('Senha muito curta!')

    if not isinstance(senha,str) or not re.match(padrao,senha):
        raise ValueError('Senha Inválido')

    #--------criptografando a senha-------------------------------
    senha_hash=bcrypt.generate_password_hash(senha).decode("utf-8")

    return senha_hash