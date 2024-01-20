from flask import Flask, render_template, redirect, request, url_for, session
import os
import requests
import secrets
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)  # Génère une clé secrète hexadécimale de 32 caractères (16 octets)

# Obtenez le chemin absolu du répertoire des modèles
template_dir = os.path.abspath('templates')
app.template_folder = template_dir

# Configurez le dossier statique
static_dir = os.path.abspath('static')
app.static_folder = static_dir
app.static_url_path = '/static'

# Middleware pour vérifier l'authentification
def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('signin'))
        return route_function(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    
    return render_template('index.html', access_token=access_token, user=user_info)

# Route pour afficher le formulaire de connexion
@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('signin.html')

# Page de connexion (signin)
@app.route('/signin', methods=['POST'])
def signin():
    # Récupérer les données du formulaire
    username = request.form.get('username')
    password = request.form.get('password')

    # Construire les données à envoyer à votre API
    data = {
        'username': username,
        'password': password
    }

    # URL de votre API de login
    api_url = 'http://10.11.5.97:8000/auth/login'

    try:
        # Envoyer la requête POST à l'API
        response = requests.post(api_url, json=data)

        # Traiter la réponse de l'API
        if response.status_code == 200:
            # Authentification réussie, récupérer les données de la réponse JSON
            response_data = response.json()
            # Stocker l'access_token et les informations de l'utilisateur dans la session
            session['access_token'] = response_data.get('access_token')
            session['user_info'] = response_data.get('user')
            
            # Rediriger vers la page souhaitée (index)
            return redirect(url_for('index_admin'))
        else:
            # Authentification échouée, afficher un message d'erreur
            return render_template('signin.html', error_message='Invalid credentials')
    except requests.RequestException as e:
        print(f"Error making request to API: {e}")
        return "Error making request to API", 500  # Réponse d'erreur interne du serveur


# Route pour afficher le formulaire d'enregistrement
@app.route('/signup', methods=['GET'])
def signup_form():
    return render_template('signup.html')

# Page d'enregistrement (signup)
@app.route('/signup', methods=['POST'])
def signup():
    # Récupérer les données du formulaire
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    email = request.form.get('email')
    birth_date = request.form.get('birth_date')

    # Construire les données à envoyer à votre API
    data = {
        'username': username,
        'password': password,
        'name': name,
        'email': email,
        'birth_date': birth_date,
    }

    # URL de votre API de login
    api_url = 'http://10.11.5.97:8000/auth/register'

    try:
        # Envoyer la requête POST à l'API
        response = requests.post(api_url, json=data)

        # Traiter la réponse de l'API
        if response.status_code == 201:
            # Authentification réussie, rediriger vers la page souhaitée (index)
            return redirect(url_for('signin'))
        else:
            # Authentification échouée, afficher un message d'erreur
            return render_template('signup.html', error_message='Invalid credentials')
    except requests.RequestException as e:
        print(f"Error making request to API: {e}")
        return "Error making request to API", 500  # Réponse d'erreur interne du serveur


@app.route('/admin/edit-user', methods=['GET'])
@login_required
def edit_user():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    return render_template('/admin/edit-user.html', access_token=access_token, user=user_info)

@app.route('/admin/users', methods=['GET'])
@login_required
def admin_users():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    return render_template('/admin/users.html', access_token=access_token, user=user_info)

@app.route('/admin/add-item', methods=['GET'])
@login_required
def add_item():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    return render_template('/admin/add-item.html', access_token=access_token, user=user_info)


@app.route('/admin/index', methods=['GET'])
@login_required
def index_admin():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    return render_template('/admin/index.html', access_token=access_token, user=user_info)

# Route de déconnexion (logout)
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    # Supprimer les informations d'authentification de la session
    session.pop('access_token', None)
    session.pop('user_info', None)
    return redirect(url_for('signin'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    # Récupérer les données du formulaire
    username = request.form.get('username')
    email = request.form.get('email')
    name = request.form.get('name')
    birth_date = request.form.get('birth_date')

    # Construire les données à envoyer à votre API (ajoutez d'autres champs au besoin)
    data = {
        'user_id': session['user_info']['id'],  # Assurez-vous que votre session contient l'ID de l'utilisateur
        'username': username,
        'email': email,
        'name': name,
        'birth_date': birth_date
    }

    # URL de votre API pour mettre à jour le profil
    api_url = 'http://10.11.5.97:8000/update_profile'  # Assurez-vous d'utiliser la bonne URL

    try:
        # Envoyer la requête POST à l'API
        response = requests.post(api_url, json=data)

        # Vérifier si la requête a réussi (code 2xx)
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return 'Failed to update profile'

    except requests.RequestException as e:
        print(f"Error making request to API: {e}")
        return "Error making request to API", 500  # Réponse d'erreur interne du serveur


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/error_404')
def error_404():
    return render_template('error_404.html')

@app.route('/catalog1')
def catalog1():
    return render_template('catalog1.html')

@app.route('/catalog2')
def catalog2():
    return render_template('catalog2.html')

@app.route('/details1')
def details1():
    return render_template('details1.html')

@app.route('/details2')
def details2():
    return render_template('details2.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)