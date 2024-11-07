import sqlite3
from bancodados import db_file, registrar_alteracao

class Computador:
    def __init__(self, ip, porta, opcoes, usuario, senha, usuario_id):
        self.ip = ip
        self.porta = porta
        self.opcoes = opcoes
        self.usuario = usuario
        self.senha = senha
        self.usuario_id = usuario_id

    def adicionar(self):
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO computadores (ip, porta, opcoes, usuario, senha, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.ip, self.porta, self.opcoes, self.usuario, self.senha, self.usuario_id))
            conn.commit()
            registrar_alteracao('computadores', 'ip', None, self.ip)

class Aplicacao:
    def __init__(self):
        self.computador = Computador('192.168.1.100', 3389, 'RDP', 'admin', 'password', 1)

    def run(self):
        self.computador.adicionar()
        print("Computador adicionado com sucesso!")

if __name__ == "__main__":
    app = Aplicacao()
    app.run()