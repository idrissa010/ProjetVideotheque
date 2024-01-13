# app2/__init__.py
from flask import Flask
from app2.controllers.auth_controller import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py', silent=True)  # Modifiez le chemin relatif ici

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
