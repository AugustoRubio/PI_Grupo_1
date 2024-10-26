# Biblioteca para instalar: pip install PyQt5
import sys
import os
import random
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
try:
    from bancodados import BancoDeDados  # Ensure this module is available and contains the required functions
except ImportError:
    class BancoDeDados:
        def __init__(self, db_file):
            self.db_file = db_file

        def check_db_integrity(self):
            # Placeholder method for checking database integrity
            return True

        def create_db(self):
            # Placeholder method for creating the database
            pass

# Diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho do banco de dados na mesma pasta que o script
db_file = os.path.join(script_dir, 'db.sqlite3')

# Classe para gerenciar a comunicação com o banco de dados
class GerenciadorBancoDeDados:
    def __init__(self, db_file):
        self.db_file = db_file
        self.banco = BancoDeDados(self.db_file)
        self.verificar_ou_criar_banco()

    def verificar_ou_criar_banco(self):
        if not os.path.exists(self.db_file) or not self.banco.check_db_integrity():
            if os.path.exists(self.db_file):
                os.remove(self.db_file)
            self.banco.create_db()

# Instancia o gerenciador do banco de dados
gerenciador_bd = GerenciadorBancoDeDados(db_file)

# Início da Janela Principal
class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Janela Principal")
        self.setFixedSize(400, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.selecionar_dispositivo_button = QPushButton("Selecionar Dispositivo", self)
        layout.addWidget(self.selecionar_dispositivo_button)

        self.adicionar_remover_dispositivo_button = QPushButton("Adicionar/Remover Dispositivo", self)
        layout.addWidget(self.adicionar_remover_dispositivo_button)

        self.historico_eventos_button = QPushButton("Histórico de Eventos", self)
        layout.addWidget(self.historico_eventos_button)

        self.sair_button = QPushButton("Sair", self)
        self.sair_button.clicked.connect(self.confirmar_saida)
        layout.addWidget(self.sair_button)

        layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.center()

    def center(self):
        frame_geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def confirmar_saida(self):
        reply = QMessageBox.question(self, 'Confirmação de Saída', 'Você tem certeza que deseja sair?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Confirmação de Saída', 'Você tem certeza que deseja sair?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
# Fim da Janela Principal

# Início da Tela de Carregamento
class TelaCarregamento(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carregando")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images', 'loading_image.png'))
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        self.central_widget.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_progresso)
        self.progresso = 0
        self.timer.start(random.randint(40, 70))  # Intervalo aleatório entre 4 a 7 segundos

    def atualizar_progresso(self):
        self.progresso += 1
        self.progress_bar.setValue(self.progresso)
        if self.progresso >= 100:
            self.timer.stop()
            self.close()
            self.tela_login = TelaLogin()
            self.tela_login.show()
# Fim da Tela de Carregamento

# Início da Tela de Login
class TelaLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images', 'login_logo.png'))
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.username_description = QLabel("Digite seu nome de usuário:", self)
        layout.addWidget(self.username_description)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Usuário")
        layout.addWidget(self.username_input)

        self.password_description = QLabel("Digite sua senha:", self)
        layout.addWidget(self.password_description)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.verificar_login)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.verificar_login)
        layout.addWidget(self.login_button)

        self.central_widget.setLayout(layout)

    def verificar_login(self):
        usuario = self.username_input.text()
        senha = self.password_input.text()

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
            resultado = cursor.fetchone()

        if resultado:
            self.close()
            self.janela_principal = JanelaPrincipal()
            self.janela_principal.show()
        else:
            QMessageBox.critical(self, "Erro", "Falha no login")
# Fim da Tela de Login

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_carregamento = TelaCarregamento()
    tela_carregamento.show()
    sys.exit(app.exec_())
