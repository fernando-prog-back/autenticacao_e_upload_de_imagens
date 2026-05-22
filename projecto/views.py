from projecto import app
from flask import render_template, request, jsonify
from projecto.controllers.admin.admin import criar_admin


@app.route('/')
def homepage():
    return render_template('user/user.html')

# Endpoint para criar um admin
@app.route('/admin', methods=['POST'])
def criar_admin_endpoint():
    # Extrair dados do formulário e arquivo
    dados = request.form.to_dict()
    file = request.files.get('foto')

    # Se nenhum arquivo for enviado, usar uma imagem padrão
    if file is None:
        file = 'default.jpeg'

    # Criar o admin usando a função do controller
    try:
        criar_admin(dados, file)
        return jsonify({"message": "Admin criado com sucesso!"}), 201
    
    # Capturar erros de validação e outros erros gerais
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    
    # Capturar erros inesperados
    except Exception as e:
        return jsonify({"error": f"Erro ao criar admin: {e}"}), 500