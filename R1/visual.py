import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QProcess, Qt
from PyQt5.QtGui import QKeySequence
from bitlocker import BitLockerManager  # Import the BitLockerManager class

# Database file
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

class LoginWindow(QWidget):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.resize(300, 150)
        self.center()

        layout = QVBoxLayout()

        self.user_label = QLabel('Usuário:', self)
        layout.addWidget(self.user_label)

        self.user_input = QLineEdit(self)
        layout.addWidget(self.user_input)

        self.pass_label = QLabel('Senha:', self)
        layout.addWidget(self.pass_label)

        self.pass_input = QLineEdit(self)
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.login_button.setShortcut(QKeySequence(Qt.Key_Return))  # Add shortcut for Enter key

        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def check_login(self):
        usuario = self.user_input.text()
        senha = self.pass_input.text()

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
            result = cursor.fetchone()

        if result:
            self.login_successful.emit()
            self.close()
        else:
            QMessageBox.warning(self, 'Erro', 'Usuário ou senha incorretos')

class BitLockerGUI(QWidget):
    authorization_completed = pyqtSignal()  # Define a signal for authorization completion

    def __init__(self):
        super().__init__()

        self.manager = BitLockerManager()  # Instantiate the BitLockerManager
        self.manager.hide_console_window()  # Hide the console window at the start
        self.initUI()

        self.authorization_completed.connect(self.show_status_window)  # Connect the signal to the slot

    def initUI(self):
        self.setWindowTitle('BitLocker Manager')
        self.resize(400, 300)
        self.center()

        layout = QVBoxLayout()

        self.status_button = QPushButton('Check BitLocker Status', self)
        self.status_button.clicked.connect(self.check_status)
        layout.addWidget(self.status_button)

        self.enable_button = QPushButton('Enable BitLocker', self)
        self.enable_button.clicked.connect(self.enable_bitlocker)
        layout.addWidget(self.enable_button)

        self.disable_button = QPushButton('Disable BitLocker', self)
        self.disable_button.clicked.connect(self.disable_bitlocker)
        layout.addWidget(self.disable_button)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().screen().rect().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def check_status(self):
        result = self.manager.check_status()
        self.output_text.append(result)
        if "Privileges elevated" in result:
            self.authorization_completed.emit()  # Emit the signal after authorization

    @pyqtSlot()
    def show_status_window(self):
        self.show()  # Show the BitLocker status window

    def enable_bitlocker(self):
        result = self.manager.enable_bitlocker()
        self.output_text.append(result)
        if "Privileges elevated" in result:
            self.authorization_completed.emit()  # Emit the signal after authorization

    def disable_bitlocker(self):
        result = self.manager.disable_bitlocker()
        self.output_text.append(result)
        if "Privileges elevated" in result:
            self.authorization_completed.emit()  # Emit the signal after authorization

if __name__ == '__main__':
    app = QApplication(sys.argv)

    login = LoginWindow()
    bitlocker_gui = BitLockerGUI()

    login.login_successful.connect(bitlocker_gui.show)
    login.show()

    sys.exit(app.exec_())
