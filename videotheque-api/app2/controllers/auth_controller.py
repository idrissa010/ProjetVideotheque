# app2/controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from app2.services.auth_service import load_users, save_users
from app2.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        name = data.get('name')
        email = data.get('email')
        birth_date_str = data.get('birth_date')  # Ajout de la birth_date

        # Convertir la chaîne de date en objet datetime
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d') if birth_date_str else None

        # Créer un utilisateur en utilisant le modèle User
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            name=name,
            email=email,
            birth_date=birth_date
        )
        # Charger les utilisateurs existants
        users = load_users()

        # Vérifier si l'utilisateur existe déjà
        if any(user.username == new_user.username for user in users):
            return jsonify({'message': 'Username already exists'}), 400

        # Ajouter le nouvel utilisateur
        users.append(new_user)

        # Sauvegarder la liste mise à jour des utilisateurs
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
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
