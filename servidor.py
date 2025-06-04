from flask import Flask, request, jsonify
from flask_cors import CORS
import banco

app = Flask(__name__)
CORS(app)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    sucesso = banco.cadastrar_usuario(nome, email, senha)
    if sucesso:
        return jsonify({'mensagem': 'Cadastro realizado com sucesso!'})
    else:
        return jsonify({'mensagem': 'Email já cadastrado.'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    sucesso = banco.fazer_login(email, senha)
    return jsonify({'login': sucesso})

if __name__ == '__main__':
    app.run(debug=True)