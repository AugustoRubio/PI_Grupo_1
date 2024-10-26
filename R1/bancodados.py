import sqlite3
import os

db_file = 'db.sqlite3'

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
        # Create your tables here
        cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            nome_completo TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        )
        ''')
        # Insert initial admin user
        cursor.execute('''
        INSERT INTO usuarios (usuario, nome_completo, email, senha)
        VALUES ('admin', 'Administrador', 'admin@example.com', 'admin')
        ''')
        conn.commit()

if not os.path.exists(db_file) or not check_db_integrity():
    if os.path.exists(db_file):
        os.remove(db_file)
    create_db()