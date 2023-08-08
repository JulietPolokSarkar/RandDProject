from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def init_db():
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            date_of_birth DATE,
            place_of_birth TEXT,
            nationality TEXT,
            gender TEXT,
            address TEXT,
            email TEXT,
            phone TEXT,
            id_photo TEXT,
            id_card TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    init_db()
    data = request.form
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (
            first_name, last_name, date_of_birth, place_of_birth,
            nationality, gender, address, email, phone, id_photo, id_card
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['first_name'], data['last_name'], data['date_of_birth'],
        data['place_of_birth'], data['nationality'], data['gender'],
        data['address'], data['email'], data['phone'],
        request.files['id_photo'].filename if 'id_photo' in request.files else '',
        request.files['id_card'].filename if 'id_card' in request.files else ''
    ))
    conn.commit()

    if 'id_photo' in request.files:
        id_photo = request.files['id_photo']
        if id_photo.filename != '':
            id_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], id_photo.filename))

    if 'id_card' in request.files:
        id_card = request.files['id_card']
        if id_card.filename != '':
            id_card.save(os.path.join(app.config['UPLOAD_FOLDER'], id_card.filename))

    conn.close()
    return redirect(url_for('index'))

@app.route('/view_data')
def view_data():
    init_db()
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('view_data.html', users=users)

# ... other routes ...

if __name__ == '__main__':
    app.run(debug=True)
