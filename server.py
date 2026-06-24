from flask import Flask, render_template_string, send_from_directory
import os
import re
from datetime import datetime

app = Flask(__name__)

PHOTO_FOLDER = "photos"
PEOPLE = "known_faces"


def extract_timestamp(filename):
    match = re.search(r'_(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})\.jpg$', filename)
    if match:
        try:
            return datetime.strptime(match.group(1), '%Y-%m-%d-%H-%M-%S')
        except ValueError:
            return datetime.min
    return datetime.min

def get_photos():
    return [f for f in os.listdir(PHOTO_FOLDER) if f.endswith('.jpg')]

@app.route('/')
def landing_page():
    return render_template_string(LANDING_TEMPLATE)

@app.route('/entries')
def show_entries():
    photos = get_photos()
    sorted_photos = sorted(photos, key=extract_timestamp, reverse=True)
    return render_template_string(ENTRIES_TEMPLATE, photos=sorted_photos)

@app.route('/people')
def show_people():
    photos = [f for f in os.listdir(PEOPLE) if f.endswith('.jpg')]
    sorted_people = sorted(photos)
    return render_template_string(PEOPLE_TEMPLATE, people=sorted_people)

@app.route('/photos/<filename>')
def uploaded_file(filename):
    return send_from_directory(PHOTO_FOLDER, filename)
    
@app.route('/known_faces/<filename>')
def saved_uploaded_file(filename):
    
    return send_from_directory(PEOPLE, filename)

# Embedded HTML templates

LANDING_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Welcome</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 100px;
            background-color: #f8f8f8;
        }
        h1 {
            font-size: 2.5em;
            color: #333;
        }
        button {
            font-size: 18px;
            padding: 12px 24px;
            margin: 10px;
            border: none;
            border-radius: 8px;
            background-color: #007BFF;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>Welcome to the PicarX Face Gallery</h1>
    <p>
        <a href="/entries"><button>View Detected Entries</button></a>
        <a href="/people"><button>View Saved People</button></a>

    </p>
</body>
</html>
"""


ENTRIES_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>All Detected Entries</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            padding: 20px;
        }
        h1, a {
            text-align: center;
            color: #333;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .photo-card {
            background: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        img {
            width: 100%;
            max-width: 200px;
            border-radius: 6px;
        }
        img.unknown {
            border: 4px solid green;
        }
        img.recognized {
            border: 4px solid red;
        }
        a {
            display: block;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>All Detected Entries</h1>
    <a href="/">⬅ Back to Home</a>
    {% if photos %}
        <div class="gallery">
        {% for photo in photos %}
            <div class="photo-card">
                <img src="{{ url_for('uploaded_file', filename=photo) }}"
                     class="{% if photo.startswith('Unknown_') %}recognized{% else %}unknown{% endif %}">
                <p>{{ photo }}</p>
            </div>
        {% endfor %}
        </div>
    {% else %}
        <p style="text-align:center;">No entries found.</p>
    {% endif %}
</body>
</html>

"""


PEOPLE_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Saved People</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #eef2f5;
            padding: 20px;
        }
        h1, a {
            text-align: center;
            color: #333;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .photo-card {
            background: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        img {
            width: 100%;
            max-width: 200px;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <h1>Saved People</h1>
    <a href="/">⬅ Back to Home</a>
    {% if people %}
        <div class="gallery">
        {% for person in people %}
            <div class="photo-card">
                <img src="{{ url_for('saved_uploaded_file', filename=person) }}">
                <p>{{ person }}</p>
            </div>
        {% endfor %}
        </div>
    {% else %}
        <p style="text-align:center;">No people found.</p>
    {% endif %}
</body>
</html>
"""



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
