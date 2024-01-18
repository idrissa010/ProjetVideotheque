from flask import Flask, render_template, redirect, request, url_for
import os
import requests
app = Flask(__name__)

# Obtenez le chemin absolu du répertoire des modèles
template_dir = os.path.abspath('templates')
app.template_folder = template_dir

# Configurez le dossier statique
static_dir = os.path.abspath('static')
app.static_folder = static_dir
app.static_url_path = '/static'

# Gestion globale des erreurs
@app.errorhandler(Exception)
def handle_error(e):
    print(f"An error occurred: {e}")
    return "Internal Server Error", 500  # Réponse d'erreur interne du serveur


@app.route('/')
def index():
    return render_template('index.html')

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
    api_url = 'http://10.11.5.81:8000/auth/login'

    try:
        # Envoyer la requête POST à l'API
        response = requests.post(api_url, json=data)

        # Traiter la réponse de l'API
        if response.status_code == 200:
            # Authentification réussie, rediriger vers la page souhaitée (index)
            return redirect(url_for('index'))
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

    # Construire les données à envoyer à votre API
    data = {
        'username': username,
        'password': password
    }

    # URL de votre API de login
    api_url = 'http://10.11.5.81:8000/auth/register'

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

@app.route('/admin/index')
def index_admin():
    return render_template('/admin/index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)