from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="event_management"
)
cursor = db.cursor()

# Image Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Routes
@app.route('/')
def index():
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    name = request.form['name']
    description = request.form['description']
    image = request.files['image']
    
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
    
    cursor.execute("INSERT INTO events (name, description, image) VALUES (%s, %s, %s)", (name, description, filename))
    db.commit()
    return redirect(url_for('index'))

@app.route('/book_event', methods=['POST'])
def book_event():
    event_id = request.form['event_id']
    name = request.form['name']
    email = request.form['email']
    cursor.execute("INSERT INTO bookings (event_id, name, email) VALUES (%s, %s, %s)", (event_id, name, email))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

