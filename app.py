from flask import Flask, jsonify, request
import pyodbc

app = Flask(__name__)

conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:sqlczu.database.windows.net,1433;DATABASE=czupsqlpiotr;UID=piotr;PWD=Jt3DMrZt68Hhpo;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def get_db_connection():
    return pyodbc.connect(conn_str)

AUTHORIZED_TOKEN = "sekretny_token"

def authorize_request(token):
    return token == AUTHORIZED_TOKEN

@app.route('/api/records', methods=['POST'])
def create_record():
    if authorize_request(request.headers.get('Authorization')):
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        conn.close()

        return jsonify({"message": "Record created"}), 201
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/records', methods=['GET'])
def read_records():
    if authorize_request(request.headers.get('Authorization')):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        records = cursor.fetchall()
        result = [{"id": row[0], "name": row[1], "age": row[2]} for row in records]
        conn.close()

        return jsonify(result), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/records/<int:id>', methods=['PUT'])
def update_record(id):
    if authorize_request(request.headers.get('Authorization')):
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET name = ?, age = ? WHERE id = ?', (name, age, id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Record updated"}), 200
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/records/<int:id>', methods=['DELETE'])
def delete_record(id):
    if authorize_request(request.headers.get('Authorization')):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Record deleted"}), 200
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run()
