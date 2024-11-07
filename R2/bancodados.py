import sqlite3
import os
from datetime import datetime

# Obtém o diretório do script
script_dir = os.path.dirname(__file__)
db_file = os.path.join(script_dir, 'db.sqlite3')

def check_db_integrity():
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            if result[0] != 'ok':
                return False
            return True
    except sqlite3.DatabaseError:
        return False

def create_db():
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        # Cria a tabela usuarios
        cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            nome_completo TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
        ''')
        # Insere o usuário admin inicial
        cursor.execute('''
        INSERT INTO usuarios (usuario, nome_completo, email, senha)
        VALUES ('admin', 'Administrador', 'admin@example.com', 'admin')
        ''')
        
        # Cria a tabela computadores
        cursor.execute('''
        CREATE TABLE computadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            porta INTEGER NOT NULL,
            opcoes TEXT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
        ''')
        
        # Cria a tabela alteracoes
        cursor.execute('''
        CREATE TABLE alteracoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tabela TEXT NOT NULL,
            coluna TEXT NOT NULL,
            valor_antigo TEXT,
            valor_novo TEXT,
            data_hora TEXT NOT NULL
        )
        ''')
        
        conn.commit()

def registrar_alteracao(tabela, coluna, valor_antigo, valor_novo):
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')  # Formato PT-BR
        cursor.execute('''
        INSERT INTO alteracoes (tabela, coluna, valor_antigo, valor_novo, data_hora)
        VALUES (?, ?, ?, ?, ?)
        ''', (tabela, coluna, valor_antigo, valor_novo, data_hora))
        conn.commit()

# Verifica se o arquivo do banco de dados existe ou se a integridade do banco de dados está comprometida
if not os.path.exists(db_file) or not check_db_integrity():
    if os.path.exists(db_file):
        os.remove(db_file)  # Remove o arquivo do banco de dados se ele existir
    create_db()  # Cria um novo banco de dados