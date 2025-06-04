import psycopg2
from psycopg2 import sql, errors
from flask import Flask

app = Flask(__name__)

# Conexão com o banco PostgreSQL
conn = psycopg2.connect(
    host="localhost",       # ou seu host remoto
    port="5432",            # porta padrão do PostgreSQL
    dbname="cadastro",     # nome do seu banco de dados
    user="postgres",     # seu usuário do PostgreSQL
    password="123"    # sua senha
)
cursor = conn.cursor()

# Criação da tabela, se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')
conn.commit()

# Função para cadastrar usuário
def cadastrar_usuario(nome, email, senha):
    try:
        cursor.execute(
            'INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)',
            (nome, email, senha)
        )
        conn.commit()
        return True
    except errors.UniqueViolation:
        conn.rollback()
        return False
    except Exception as e:
        print("Erro:", e)
        conn.rollback()
        return False

# Função para login
def fazer_login(email, senha):
    cursor.execute(
        'SELECT * FROM usuarios WHERE email = %s AND senha = %s',
        (email, senha)
    )
    usuario = cursor.fetchone()
    return usuario is not None