from flask import Flask

class Config:
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/0'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes import main
    app.register_blueprint(main)

    return app