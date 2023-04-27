import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('users.db')
    return db

class UserDataBase:
    def __init__(self):
        self.cursor = get_db().cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            phone_number TEXT NOT NULL)''')
        get_db().commit()

    def insert_user(self, name, phone_number):
        self.cursor.execute(f"INSERT INTO users (name, phone_number) VALUES ('{name}', '{phone_number}')")
        get_db().commit()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        return [{'id': row[0], 'name': row[1], 'phone_number': row[2]} for row in rows]

    def get_user(self, name):
        self.cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
        row = self.cursor.fetchone()
        if row is None:
            return None
        return {'id': row[0], 'name': row[1], 'phone_number': row[2]}

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data['Name']
    phone_number = data['Phone Number']
    db = UserDataBase()
    db.insert_user(name, phone_number)
    return jsonify({'message': 'User added successfully'})

@app.route('/get-users', methods=['GET'])
def get_users():
    db = UserDataBase()
    users = db.get_all_users()
    return jsonify(users)

@app.route('/get-user/<name>', methods=['GET'])
def get_user(name):
    db = UserDataBase()
    user = db.get_user(name)
    if user is None:
        return jsonify({'message': 'User not found'})
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)
