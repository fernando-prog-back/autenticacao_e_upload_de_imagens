from app import app,db,bcrypt
from app.models import User,Book, Capitulo , Materia,Pagina
from app.min_service.verificacao import validar_email,validar_senha
from app.min_service.upload_file import upload

from flask import request, jsonify, url_for,flash,render_template
from flask_login import current_user, logout_user, login_user, login_required


#============================================================
#================CADASTRO DE USUARIOS========================
#============================================================
@app.route('/cadastrar', methods=['GET','POST'])
def cadastrar():  
    try:
        if request.method == 'POST':
            # pengandos os dados enviados e tranformar em dicionário
            dados = request.form.to_dict()

            file=request.files.get('foto')
            print(file)

            # verificando se o dados foi fornecido
            if not dados:
                return flash('Nenhum dado fornecido.','danger'), 400
            
            #checando se os campos obrigatórios existem
            required_fields=['username' , 'email', 'senha']

            for field in required_fields:
                if field not in dados:
                    return flash(f'Campo {field} é obrigatório','danger'), 400

            if any(char.isdigit() for char in dados.get('username')):
                return flash('O campo Username deve Ser apenas Letras','danger')
            
            #-------------verificando o email------------------
            try:         
                valid_email = validar_email(dados.get('email'))
            except ValueError as e:
                return flash(str(e)),400


            #------------verificando a senha-------------
            try:         
                valid_senha=validar_senha(dados.get('senha'))
            except ValueError as e:
                return flash(str(e),'danger'),400
            
            # fazendo o upload da imagem.
            if file:
                filename = upload(file=file)

            usuario = User(
                username=dados.get('username'),
                email=valid_email,
                password=valid_senha,
                image = filename  if file else 'default.jpeg',
            )
            db.session.add(usuario)
            db.session.commit()
            
            return flash('Cadastro Feito com Sucesso.','danger'),201
        
        return render_template('index.html')
    
    except Exception as e:
        return flash(f'erro no codigo. {e}','danger')

@app.route('/login', methods=['POST'])
def login():
    try:

        if request.method == "POST":

            data = request.form.to_dict()

            email = data.get("username")
            password = data.get("password")

            if not email or not password:
                raise ValueError('Preencha todos os campos corretamente!')
            
            user = User.query.filter_by(email=email).first()

            senha_hash = bcrypt.check_password_hash(user.password,password)

            if user and senha_hash == password: 

                login_user(user, remember = True)
            
            else:
                raise ValueError('Erro Nas Credênciais')

    except Exception as e:

        return flash(f'{str(e)}', 'danger')

#====================================================
#=================Criar problemas====================
#====================================================
@app.route("/usuario/<int:user_id>/caderno", methods=["POST"])
@login_required
def criar_caderno(user_id):

    user = User.query.get(user_id)
    data = request.form

    disciplina = data.get("disciplina")
    curso = data.get("curso")
    classe = data.get("classe")
    ano_lectivo = data.get("ano_lectivo").lower()

    print(disciplina, ano_lectivo)

    # validação básica
    CAMPOS_REQUIRED = ['disciplina', 'curso', 'classe', 'ano_lectivo']

    for field in CAMPOS_REQUIRED:
        if field not in data:
            return flash(f'Campo {field} é obrigatório'),400

    book = Book(
        disciplina = disciplina,
        curso = curso,
        classe = classe,
        Ano_lectivo = ano_lectivo 
    )
    db.session.add(book)
    db.session.commit()

    return flash('Caderno criado!','success'), 201
