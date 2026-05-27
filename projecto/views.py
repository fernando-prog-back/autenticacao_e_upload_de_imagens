from projecto import app
from flask import render_template, request, jsonify
from projecto.controllers.admin.admin import criar_admin
from projecto.controllers.microservice.upload import upload


@app.route('/')
def homepage():
    return render_template('cadastro.html')

# Endpoint para criar um admin
@app.route('/create/admin', methods=['POST', 'GET'])
def criar_admin_endpoint():
    if request.method == 'POST':
        # Extrair dados do formulário e arquivo
        dados = request.form.to_dict()
        file = request.files.get('picture')

        filename = upload(file=file)
        # Criar o admin usando a função do controller
        try:
            criar_admin(dados, filename) 

            return jsonify({"message": "Admin criado com sucesso!"}), 201
        
        # Capturar erros de validação e outros erros gerais
        except ValueError as ve:
            return jsonify({"sms": str(ve)}), 400
        
        # Capturar erros inesperados
        except Exception as e:
            return jsonify({"sms": f"Erro ao criar admin: {e}"}), 500
        
    return render_template('cadastro.html')