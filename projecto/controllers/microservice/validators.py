from projecto.models import Usuario, Admin
from projecto import bcrypt
import re

# validar email
def validar_email(email):
    
    # O email deve ser do tipo string e seguir o formato específico
    padrao = r'^[a-zA-Z0-9]+@(gmail\.com|hotmail\.com)$'
    if not isinstance(email,str) or not re.match(padrao,email):
        raise ValueError('E-mail Inválido  dsdfs')

    # Verificar se o email já existe na tabela Usuario ou Admin
    if Usuario.query.filter_by(email=email).first() or Admin.query.filter_by(email=email).first():
        raise ValueError('E-mail Inválido')
   
    # Retornar o email em letras minúsculas para consistência
    return email.lower()

    
# validar senha
def validar_senha(senha):

    # A senha deve conter entre 8 e 16 caracteres, incluindo letras, números e caracteres especiais
    padrao = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,16}$'
    if len(senha) < 8:
        raise ValueError('Senha muito curta!')

    
    if not isinstance(senha,str) or not re.match(padrao,senha):
        raise ValueError('Senha Inválido')

    #--------criptografando a senha-------------------------------
    senha_hash=bcrypt.generate_password_hash(senha).decode("utf-8")

    # Retornar a senha criptografada
    return senha_hash