from flask import Blueprint, jsonify
from app.tasks import dizer_ola

main = Blueprint('main', __name__)

@main.route('/test')
def test():
    dizer_ola.delay()
    return jsonify({"msg": "Tarefa enviada para o Celery"})