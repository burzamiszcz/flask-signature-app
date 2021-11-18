from flask import Flask, jsonify, request
import requests
import sqlite3
import os
app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['POST', 'GET'])
def login():
    username = request.json['username']
    password = request.json['password']

    if username:
        conn = sqlite3.connect('users.db')
        conn.row_factory = dict_factory
        c = conn.cursor()  
        c.execute(f"SELECT * FROM users WHERE username='{username}'")
        user = c.fetchone()
        c.close()
    try:
        if user:
            if password == user['password']:
                return jsonify({'credential': user['credential'], 'id': user['id'], 'username': user['username']})
    except: 
        return jsonify({"credential": None})

    return jsonify({"credential": None})


@app.route('/new_user', methods=['POST', 'GET'])
def new_user():
    # username = request.json['username']
    # password = request.json['password']
    # credential = request.json['credential'] 
    username = 'admin23'
    password = 'admin23'
    credential = 'admin'
    conn = sqlite3.connect('/app/users.db')
    conn.row_factory = dict_factory
    c = conn.cursor()  
    c.execute(f"SELECT * FROM users WHERE username='{username.lower()}'")
    user = c.fetchone()
    c.close()
    if user == None:
        conn = sqlite3.connect('/app/users.db')
        c = conn.cursor()  
        c.execute(f"INSERT INTO users (username, password, credential) VALUES ('{username}', '{password}', '{credential}')")
        print('poszlo', flush=True)
        conn.commit()
        return jsonify({"status": "created"}) 
    else:
        return jsonify({"status": "exist"})

if __name__ == '__main__':
    app.run()
