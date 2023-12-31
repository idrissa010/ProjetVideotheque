from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__, template_folder='/home/toto/ProjetVideotheque/videotheque/templates')

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
        return f"Error loading JSON data: {json_file_path}\nError: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
