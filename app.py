from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'twoj_tajny_klucz' 

conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=tcp:34.69.79.232,1433;DATABASE=master;UID=sqlserver;PWD=Haslo123.;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

def get_db_connection():
    return pyodbc.connect(conn_str)

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        name = request.form.get('name')
        age = request.form.get('age')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
        conn.commit()
        conn.close()
        
        flash('Użytkownik został dodany pomyślnie!', 'success')
    except Exception as e:
        flash(f'Wystąpił błąd podczas dodawania użytkownika: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_user/<int:id>')
def delete_user(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        flash('Użytkownik został usunięty pomyślnie!', 'success')
    except Exception as e:
        flash(f'Wystąpił błąd podczas usuwania użytkownika: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
