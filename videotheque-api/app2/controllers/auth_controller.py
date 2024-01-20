# app2/controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from app2.services.auth_service import load_users, save_users
from app2.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import json

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        email = data.get('email')
        #birth_date = data.get('birth_date')
        birth_date_str = data.get('birth_date')

        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d') if birth_date_str else None

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            name=name,
            email=email,
            birth_date=birth_date
        )

        users = load_users()

        if any(user.username == new_user.username for user in users):
            return jsonify({'message': 'Username already exists'}), 400

        users.append(new_user)
        save_users(users)

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'Error during registration: {str(e)}'}), 500



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()
    user = next((user for user in users if user.username == username), None)

    if user and check_password_hash(user.password, password):
        # Utiliser Flask-JWT-Extended pour créer un jeton d'accès
        access_token = create_access_token(identity=user.id)
        # Formater la date en "dd-mm-yyyy"
        formatted_birth_date = user.birth_date.strftime('%d/%m/%Y') if user.birth_date else None
        # Retourner les informations de l'utilisateur connecté sans le mot de passe
        user_info = {key: getattr(user, key) for key in ['id', 'username', 'name', 'email', 'role']}
        user_info['birth_date'] = formatted_birth_date
        return jsonify({'message': 'Login successful', 'access_token': access_token, 'user': user_info}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

    
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()  # Cette route nécessite un jeton valide
def protected():
    # Obtenir l'identité de l'utilisateur actuel
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
