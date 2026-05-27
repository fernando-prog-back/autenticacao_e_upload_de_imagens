from estudo import app
from flask import jsonify

@app.route('/')
def homepage():
    dados = {'dados':"Ola, mundo!"}
    return jsonify(dados)  