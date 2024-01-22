# app2/models/user.py
from datetime import datetime
import uuid

class User:
    def __init__(self, username, password, name, email, birth_date=None, role='user', id=None):
        self.id = id #if id else str(uuid.uuid4())   # Génère un UUID unique
        self.username = username
        self.password = password
        self.created_at = datetime.now()

        if birth_date is not None:
            if isinstance(birth_date, str):
                # Convertir la chaîne de date en objet datetime
                self.birth_date = datetime.strptime(birth_date, '%d-%m-%Y')
            elif isinstance(birth_date, datetime):
                self.birth_date = birth_date
            else:
                raise ValueError("Invalid birth_date format")
        else:
            self.birth_date = None

        self.name = name
        self.email = email
        self.role = role
        self.status = 'active'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'birth_date': self.birth_date.strftime('%d-%m-%Y') if self.birth_date else None,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'status': self.status
        }
