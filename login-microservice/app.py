from flask import Flask, jsonify, request
import requests
import sqlite3

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


if __name__ == '__main__':
    app.run()
