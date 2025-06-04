import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

conn = sqlite3.connect('usuarios.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
''')
conn.commit()

def cadastrar_usuario(nome, email, senha):
    try:
        cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def fazer_login(email, senha):
    cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
    usuario = cursor.fetchone()
    return usuario is not None

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')
    
    if fazer_login(email, senha):
        return jsonify({'status': 'success', 'message': 'Login bem-sucedido!'})
    else:
        return jsonify({'status': 'error', 'message': 'Credenciais inválidas.'}), 401

if __name__ == '__main__':
    app.run(debug=True)