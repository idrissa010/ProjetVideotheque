from flask import Flask, render_template, redirect, request, url_for, session, jsonify
import os
import requests
import secrets
from functools import wraps
import json

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



@app.route('/dashboard/edit-user', methods=['GET'])
@login_required
def edit_user():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    return render_template('/admin/edit-user.html', access_token=access_token, user=user_info)


@app.route('/add_movie', methods=['POST'])
@login_required
def add_movie():
    # Récupérer les informations de l'utilisateur connecté à partir de la session
    access_token = session.get('access_token')
    user_info = session.get('user_info', {})
    owner_id = user_info.get('id')
    
    # Récupérer les données du formulaire
    title = request.form.get('title')
    description = request.form.get('description')
    release_year = request.form.get('release_year')
    duration = request.form.get('duration')
    quality = request.form.get('quality')
    age = request.form.get('age')
    country = request.form.getlist('country')
    genre = request.form.getlist('genre')
    category = request.form.get('category')
    rating = request.form.get('rating')
    
    # Vérifier si un ID de film est fourni dans la requête
    movie_id = request.form.get('movie_id')

    # Construire les données à envoyer à votre API
    data = {
        'owner_id': owner_id,
        'title': title,
        'description': description,
        'release_year': release_year,
        'duration': duration,
        'quality': quality,
        'age': age,
        'country': country,
        'genre': genre,
        'category': category,
        'rating': rating,
    }
    
     # Construire l'en-tête de la requête avec le token JWT
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # URL de votre API pour ajouter ou mettre à jour un film ou une série TV
    api_url = 'http://10.11.5.97:8000/video/videos'
    
    # Si movie_id est fourni, cela signifie que vous effectuez une mise à jour
    if movie_id:
        api_url += f'/{owner_id}/{movie_id}'

    try:
        # Envoyer la requête POST ou PUT à l'API en fonction de si movie_id est fourni
        if movie_id:
            response = requests.put(api_url, json=data, headers=headers)
        else:
            response = requests.post(api_url, json=data, headers=headers)

        # Traiter la réponse de l'API
        if response.status_code == 201 or response.status_code == 200:
            # Ajout ou mise à jour réussi, rediriger vers la page souhaitée
            return redirect(url_for('movies'))
        else:
            # Échec de l'ajout ou de la mise à jour, afficher un message d'erreur
            return redirect(url_for('add_item'))
    except requests.RequestException as e:
        print(f"Error making request to API: {e}")
        return "Error making request to API", 500  # Réponse d'erreur interne du serveur



@app.route('/edit_movie/<movie_id>', methods=['GET'])
@login_required
def edit_movie(movie_id):
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    videos = session.get('videos')  # Récupérer les vidéos depuis la session
    
    if not access_token or not user_info:
        return redirect(url_for('signin'))   
     
    # Charger les données des pays depuis le fichier JSON
    with open('data/countries.json', 'r') as json_file:
        countries_data = json.load(json_file)
        
    # Rechercher la vidéo avec movie_id dans les vidéos de la session
    movie_info = next((video for video in videos if video['id'] == movie_id), None)

    if movie_info:
        return render_template('/admin/add-item.html', access_token=access_token, user=user_info, movie=movie_info, countries=countries_data)
    else:
        # flash('Failed to retrieve movie details', 'error')
        return redirect(url_for('movies'))



@app.route('/delete_movie/<movie_id>', methods=['DELETE', 'POST'])
@login_required
def delete_movie(movie_id):
    if request.method == 'POST' and request.form.get('_method') == 'DELETE':
        # Récupérer l'ID du propriétaire connecté
        access_token = session.get('access_token')
        owner_id = session.get('user_info', {}).get('id')

        # Vérifier si l'ID du film et l'ID du propriétaire sont valides
        if not owner_id or not movie_id:
            return jsonify({'error': 'Invalid movie ID or owner ID'}), 400

        # Construire l'en-tête de la requête avec le token JWT
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Construire l'URL de l'API pour la suppression du film
        api_url = f'http://10.11.5.97:8000/video/videos/{owner_id}/{movie_id}'

        try:
            # Envoyer la requête DELETE à l'API
            response = requests.delete(api_url, headers=headers)

            # Traiter la réponse de l'API
            if response.status_code == 200:
                return redirect(url_for('movies'))
                # return jsonify({'message': 'Movie deleted successfully'}), 200
            else:
                return jsonify({'error': 'Failed to delete movie'}), response.status_code
        except requests.RequestException as e:
            print(f"Error making request to API: {e}")
            return jsonify({'error': 'Failed to make request to API'}), 500

    # Retourner une erreur si la méthode n'est pas autorisée
    return jsonify({'error': 'Method not allowed'}), 405



@app.route('/dashboard/movies', methods=['GET'])
@login_required
def movies():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    
    # Construire l'en-tête de la requête avec le token JWT
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Récupérer les vidéos de l'utilisateur via l'API en backend
    owner_id = user_info.get('id')
    api_url = f'http://10.11.5.97:8000/video/videos/{owner_id}'
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        videos = response.json()     
        # Stocker les vidéos dans la session Flask
        session['videos'] = videos
    else:
        videos = []  # Gérer l'erreur si la récupération des vidéos échoue
        
    # Passer les vidéos à votre modèle pour les afficher
    return render_template('/admin/movies.html', access_token=access_token, user=user_info, videos=videos)



@app.route('/dashboard/users', methods=['GET'])
@login_required
def admin_users():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    return render_template('/admin/users.html', access_token=access_token, user=user_info)

@app.route('/dashboard/add-item', methods=['GET'])
@login_required
def add_item():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    
    # Charger les données des pays depuis le fichier JSON
    with open('data/countries.json', 'r') as json_file:
        countries_data = json.load(json_file)
    
    # Définir movie comme une variable vide
    movie = None
        
    return render_template('/admin/add-item.html', access_token=access_token, user=user_info, countries=countries_data,  movie=movie)


@app.route('/dashboard/index', methods=['GET'])
@login_required
def index_admin():
    # Récupérer l'access_token et les informations de l'utilisateur depuis la session
    access_token = session.get('access_token')
    user_info = session.get('user_info')
    return render_template('/admin/index.html', access_token=access_token, user=user_info)



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