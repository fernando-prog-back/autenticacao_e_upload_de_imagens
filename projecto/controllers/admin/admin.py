from projecto import db
from projecto.models import Admin
from projecto.controllers.microservice.validators import validar_email, validar_senha

# Função para criar um admin
def criar_admin(dados, file):
    try:
        # estraindo dados do dicionário dados
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")
        picture = file

        # Verificar se o email  já existe e se a senha é válida
        try:
            email_valid = validar_email(email)
            senha_hash = validar_senha(senha)
        except ValueError as ve:
            raise ValueError(ve)
        
        # Criar o objeto Admin
        novo_admin = Admin(
            nome=nome,
            email=email_valid, 
            password=senha_hash,
            picture=picture
            )

        # Adicionar ao banco de dados
        db.session.add(novo_admin)
        db.session.commit()

        print(f"Admin {nome} criado com sucesso!")

    # Capturar erros inesperados
    except Exception as e:
        print(f"Erro ao criar admin: {e}")
        # Reverter a transação em caso de erro
        db.session.rollback()    