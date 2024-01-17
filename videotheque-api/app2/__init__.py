# app2/__init__.py
from flask import Flask
from app2.controllers.auth_controller import auth_bp
from app2.controllers.video_controller import video_bp
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py', silent=True) 

    # Configurer Flask-JWT-Extended
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key' 
    jwt = JWTManager(app)

    # Enregistrez les blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(video_bp, url_prefix='/video')

    return app
