from flask import Flask, render_template
import json
import os
app = Flask(__name__)

# Obtenez le chemin absolu du répertoire des modèles
template_dir = os.path.abspath('templates')
app.template_folder = template_dir

# Configurez le dossier statique
static_dir = os.path.abspath('static')
app.static_folder = static_dir
app.static_url_path = '/static'

# Get the directory of the script
json_file_path = os.path.join('data', 'app1_data.json')

@app.route('/')
def index():
    try:
        # Load data from the JSON file
        with open(json_file_path, 'r') as json_file:
            movie_data = json.load(json_file)
        return render_template('index.html', movies=movie_data)
    except FileNotFoundError as e:
        return f"File not found: {json_file_path}\nError: {e}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON data: {json_file_path}\nError: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

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
