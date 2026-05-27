from competcode import app,db,bcrypt, UPLOAD_FOLDER
from competcode.models import User,Problema, Submissao,Resultado,Teste
from competcode.min_service.verificacao import validar_email,validar_senha
from competcode.min_service.upload_file import upload


from flask import request, jsonify, url_for
from flask_jwt_extended import (
    create_access_token,
    jwt_required, get_jwt_identity,
    create_refresh_token
)
from sqlalchemy.exc import IntegrityError



@app.route('/', methods=['GET'])
def home():
    de = Submissao.query.filter_by(id=2).first()
    print(de)

    print('deletado com sucesso!')

    return 'fwepfnwe'

#============================================================
#================CADASTRO DE USUARIOS========================
#============================================================
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
      
    try:
        # pengandos os dados enviados e tranformar em dicionário
        dados = request.form.to_dict()

        file=request.files.get('foto')
        print(file)

        # verificando se o dados foi fornecido
        if not dados:
            return jsonify({'msg':'Nenhum dado fornecido.'}), 400
        
        #checando se os campos obrigatórios existem
        required_fields=['username' , 'email', 'senha']

        for field in required_fields:
            if field not in dados:
                return jsonify({'msg':f'Campo {field} é obrigatório'}),400

        if any(char.isdigit() for char in dados.get('username')):
            return jsonify({'msg':'O campo Username deve Ser apenas Letras'})
        
        #-------------verificando o email------------------
        try:         
            valid_email = validar_email(dados.get('email'))
        except ValueError as e:
            return jsonify({'msg': str(e) }),400


        #------------verificando a senha-------------
        try:         
            valid_senha=validar_senha(dados.get('senha'))
        except ValueError as e:
            return jsonify({'msg': str(e)}),400
        
        # fazendo o upload da imagem.
        filename = upload(file=file)

        # categorias validas 'UsuarioNormal' and 'UsuarioAdministrador'    
        valid_role=["user",'admin']
        if dados.get('role').lower() not in valid_role:
            return jsonify({'msg': 'Nao existe esta categoria!'}),400
        
        usuario = User(
            username=dados.get('username'),
            email=valid_email,
            senha=valid_senha,
            image =filename,
            role=dados.get('role')
        )
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify({'msg':'Cadastro Feito com Sucesso.'}),201
        
    except Exception as e:
        return jsonify({'msg':f'erro no codigo. {e}'})


#====================================================================
#=============================LOGIN==================================
#====================================================================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        email = data.get("email")
        senha = data.get("senha")

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.senha, senha):
            raise ValueError('Erro nas credênciais')

        access_token = create_access_token(identity=str(user.id))
        if access_token is None:
            raise ValueError('Erro nas credênciais')
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "user_rule":str(user.role)
        }), 200
    except ValueError as e:
        return jsonify({'msg':str(e)})

#=============================================================
#==================PERFIL DO USUARIO==========================
#=============================================================
@app.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    print(user)

    image_url = None
    if user.image:
        image_url = url_for('static', filename=f'uploads/{user.image}', _external=True)

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "image": image_url
    })




#===============================================================
#=======================PERFIL ADM==============================
#===============================================================
@app.route("/admin/perfil", methods=["GET"])
@jwt_required()
def admin_perfil():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return jsonify({"erro": "usuário não encontrado"}), 404

    # 🚨 só admin pode acessar
    if user.role != "admin":
        return jsonify({"erro": "acesso negado"}), 403

    image_url = None
    if user.image:
        image_url = url_for('static', filename=f'uploads/{user.image}', _external=True)

    # 🧠 permissões do admin
    permissoes = [
        "criar_problemas",
        "editar_problemas",
        "deletar_problemas",
        "ver_usuarios",
        "ver_submissoes",
        "gerir_problemas"
    ]
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "image":image_url,
        "permissoes":permissoes
    }), 200



#=================================================
#====================PROMOVER USER PARA ADM==================
#=================================================
@app.route("/admin/promover", methods=["POST"])
@jwt_required()
def promote():
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if admin.role != "admin":
        return jsonify({"erro": "sem permissão"}), 403

    email = request.get_json()

    user = User.query.filter_by(email=email.get('email')).first()

    if not user:
        return jsonify({"erro": "usuário não encontrado"}), 404

    user.role = "admin"
    db.session.commit()

    return jsonify({"msg": "usuário promovido a admin"}), 200


#====================================================
#=================Criar problemas====================
#====================================================
@app.route("/admin/problemas/create", methods=["POST"])
@jwt_required()
def criar_problema():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # 🚨 só admin pode criar
    if user.role != "admin":
        return jsonify({"erro": "acesso negado"}), 403

    data = request.get_json()

  

    titulo = data.get("titulo")
    descricao = data.get("descricao")
    dificuldade = data.get("dificuldade", "facil").lower()

    # 🔥 defaults por dificuldade
    CONFIG = {
        "facil": {"tempo": 1, "memoria": 128},
        "medio": {"tempo": 2, "memoria": 256},
        "dificil": {"tempo": 3, "memoria": 512}
    }

    if dificuldade not in CONFIG:
        return jsonify({"erro": "dificuldade inválida"}), 400

    tempo_limite = CONFIG[dificuldade]["tempo"]
    memoria_limite = CONFIG[dificuldade]["memoria"]

    # validação básica
    if not titulo or not descricao:
        return jsonify({"erro": "titulo e descricao obrigatórios"}), 400
    
    problema = Problema(
        titulo=titulo,
        descricao=descricao,
        dificuldade=dificuldade,
        tempo_limite=tempo_limite,
        memoria_limite=memoria_limite
    )

    db.session.add(problema)
    db.session.commit()

    return jsonify({
        "msg": "problema criado com sucesso",
        "id": problema.id,
        "tempo_limite": tempo_limite,
        "memoria_limite": memoria_limite
    }), 201



#======================================================
#=================Ver Problemas========================
#======================================================
@app.route('/problemas', methods=['GET'])
def ver_problemas():
    # buscar todos os problemas cadastrados no banco
    problema=Problema.query.all()

    problemas=[]

    for p in problema:
        problemas.append({
            'id':p.id,
            'titulo':p.titulo,
            'descricao':p.descricao,
            'dificuldade':p.dificuldade
         })
        
    return jsonify(problemas)


#====================================================
#=================Actualizar problemas===============
#====================================================
@app.route("/admin/problemas/update/<int:id>", methods=["POST"])
@jwt_required()
def actualizar_problema(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # 🚨 só admin pode actualizar
    if user.role != "admin":
        return jsonify({"erro": "acesso negado"}), 403
    
    problema = Problema.query.filter_by(id=id).first()

    data = request.get_json()

    titulo = data.get("titulo")
    descricao = data.get("descricao")
    dificuldade = data.get("dificuldade", "facil").lower()

    # 🔥 defaults por dificuldade
    CONFIG = {
        "facil": {"tempo": 1, "memoria": 128},
        "medio": {"tempo": 2, "memoria": 256},
        "dificil": {"tempo": 3, "memoria": 512}
    }

    if dificuldade not in CONFIG:
        return jsonify({"erro": "dificuldade inválida"}), 400

    tempo_limite = CONFIG[dificuldade]["tempo"]
    memoria_limite = CONFIG[dificuldade]["memoria"]

    # validação básica
    if not titulo or not descricao:
        return jsonify({"erro": "titulo e descricao obrigatórios"}), 400
    
    problema.titulo=titulo
    problema.descricao=descricao
    problema.dificuldade=dificuldade
    problema.tempo_limite=tempo_limite
    problema.memoria_limite=memoria_limite
    
    db.session.commit()

    return jsonify({
        "msg": "problema Atualizado com sucesso",
        "id": problema.id,
        "tempo_limite": tempo_limite,
        "memoria_limite": memoria_limite
    }), 201


#====================================================
#=================Deletar problemas===============
#====================================================
@app.route("/admin/problemas/delete/<int:id>", methods=["POST"])
@jwt_required()
def deletar_problema(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    problema = Problema.query.get(2)
    # 🚨 só admin pode deletar
    if user.role != "admin":
        return jsonify({"erro": "acesso negado"}), 403
    
    #problema = Problema.query.get(id)

    if not problema:
        return jsonify({
            'msg':'Prolema nao encontrado.'
        })

    db.session.delete(problema)
    db.session.commit()

    return jsonify({
        "msg": "problema Deletado com sucesso",
    }), 201


#====================================================
#=================Cadastrar TEstes===============
#====================================================

@app.route("/problema/<int:problema_id>/teste", methods=["POST"])
@jwt_required()
def criar_teste(problema_id):

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    # =========================
    # PERMISSÃO (opcional mas importante)
    # =========================
    if not user or user.role != "admin":
        return jsonify({"error": "acesso negado"}), 403

    data = request.get_json()

    entrada = data.get("entrada")
    saida_esperada = data.get("saida_esperada")

    # =========================
    # VALIDAÇÃO
    # =========================
    if not entrada or not saida_esperada:
        return jsonify({"error": "entrada e saida_esperada obrigatórios"}), 400

    # =========================
    # VERIFICAR PROBLEMA
    # =========================
    problema = Problema.query.get(problema_id)

    if not problema:
        return jsonify({"error": "problema não encontrado"}), 404

    # =========================
    # CRIAR TESTE
    # =========================
    teste = Teste(
        problema_id=problema_id,
        entrada=entrada,
        saida_esperada=saida_esperada
    )

    db.session.add(teste)
    db.session.commit()

    return jsonify({
        "message": "teste criado com sucesso",
        "teste_id": teste.id,
        "problema_id": problema_id
    }), 201


#====================================================
#=================Receber Submissoes===============
#====================================================
@app.route("/submissoes", methods=["POST"])
@jwt_required()
def receber_submissoes():
    # importando o judge
    #from judge.judge import run_submission

    user_id = get_jwt_identity()

    # pegando os dados json submetidos 
    data = request.get_json()

    problem_id = data.get("problema_id")
    code = data.get("codigo")
    language = data.get("linguagem")


    # verificando se foi informado o id do problema e o codigo
    if not problem_id or not code:
        return jsonify({"msg": "Dados inválidos"}), 400

    # verificando se foi informado uma linguagem
    if not language:
        return jsonify({"msg": "Informe a linguagem"}), 400
    
    # VErificando se o problema existe
    problema = Problema.query.get(int(problem_id))
    if not problema:
        return jsonify({"msg": "PRoblema não Encontrado!"}), 404
    
    # verificando se problema tem testes
    if not problema.testes :
        return jsonify({"error": "Problemas sem Tstes!"}), 400
    
    # inicializando a minha instânçia da class Submissao
    submissao = Submissao(
        usuario_id=user_id,
        problema_id=problem_id,
        codigo=code,
        linguagem=language,
        tempo_execucao = problema.tempo_limite,
        memoria_usada = problema.memoria_limite
    )

    # adicionando a minha tabela submissção ao meu banco
    db.session.add(submissao)
    # Certificando o cadastro
    db.session.commit()


    # disparar o JUDGE
    #run_submission.delay(submissao.id)
    
    # retornar a resposta json para o cliente.
    return jsonify({
        "msg": "Submissão criada",
        "id": submissao.id
    }), 201

