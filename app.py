import os
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, url_for

app = Flask(__name__)

AUTHORIZED_TOKEN = "sekretny_token"

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/hello', methods=['POST'])
def hello():
    auth_token = request.headers.get('Authorization')
    
    if auth_token == AUTHORIZED_TOKEN:
        name = request.form.get('name')
        return jsonify({"message": f"Witaj, {name}!"}), 200
    else:
        return jsonify({"error": "Nieautoryzowany dostęp"}), 401

if __name__ == '__main__':
   app.run()
