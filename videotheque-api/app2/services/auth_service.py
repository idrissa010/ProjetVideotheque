# app2/services/auth_service.py
import json
from app2.models.user import User
from config import JSON_DATABASE_PATH

def load_users():
    try:
        with open(JSON_DATABASE_PATH, 'r') as file:
            users_data = json.load(file)
    except FileNotFoundError:
        users_data = []
    
    users = [User(
        username=user_data['username'],
        password=user_data['password'],
        birth_date=user_data['birth_date'],
        name=user_data['name'],
        email=user_data['email'],
        role=user_data['role']
    ) for user_data in users_data]

    print(users)  # Ajout de l'impression pour le débogage
    return users

def save_users(users):
    users_data = [user.to_dict() for user in users]
    with open(JSON_DATABASE_PATH, 'w') as file:
        json.dump(users_data, file)