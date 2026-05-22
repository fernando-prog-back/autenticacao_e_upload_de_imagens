from projecto import db
from projecto.models import Usuario
from projecto.controllers.microservice.validators import validar_email, validar_senha

# Função para criar um usuário normal
def criar_usuario(dados, file):
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
            raise ValueError(f"Erro de validação: {ve}")
        
        # Criar o objeto Usuario
        novo_usuario = Usuario(
            nome=nome,
            email=email_valid, 
            senha_hash=senha_hash,
            picture=picture
            )

        # Adicionar ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        print(f"Usuario {nome} criado com sucesso!")

    # Capturar erros inesperados
    except Exception as e:
        print(f"Erro ao criar usuario: {e}")
        # Reverter a transação em caso de erro
        db.session.rollback()    