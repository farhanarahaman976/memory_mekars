from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import os
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Database Configuration
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="event_management"
    )

# Image Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Email Validation Function
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Routes
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, image FROM events")
    events = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    name = request.form['name']
    description = request.form['description']
    image = request.files['image']
    filename = None  # Default if no image is uploaded

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (name, description, image) VALUES (%s, %s, %s)", 
                       (name, description, filename))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database Error:", e)
        return "Error adding event", 500

    return redirect(url_for('index'))

@app.route('/book_event', methods=['POST'])
def book_event():
    event_id = request.form['event_id']
    name = request.form['name']
    email = request.form['email']

    # Email validation
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email address"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bookings (event_id, name, email) VALUES (%s, %s, %s)", 
                       (event_id, name, email))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Database Error:", e)
        return "Error booking event", 500

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
