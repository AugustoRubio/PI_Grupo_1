# pip install --upgrade pip
# Biblioteca para instalar: pip install PyQt5 PyQt5-sip PyQtWebEngine
import sys
import os
import random
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QProgressBar, QTableWidget, QTableWidgetItem, QCheckBox, QInputDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
import socket
import ipaddress
import nmap
from datetime import datetime
from datetime import datetime
import socket
import ipaddress
from adicionar_disp_win import Computador  # Ensure Computador class is correctly defined in adicionar_disp_win module

# Define the BancoDeDados class if it is not already defined in the bancodados module
class BancoDeDados:
    def __init__(self, db_file):
        self.db_file = db_file

    def check_db_integrity(self):
        # Dummy implementation, replace with actual integrity check
        return True

    def create_db(self):
        # Dummy implementation, replace with actual database creation logic
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

# Define a cor de fundo e a cor da fonte em HEX
background_color = "#FFFFFF"  # Branco
font_color = "#000000"  # Preto

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
        self.selecionar_dispositivo_button.clicked.connect(self.mostrar_mensagem_manutencao)
        layout.addWidget(self.selecionar_dispositivo_button)

        self.adicionar_remover_dispositivo_button = QPushButton("Adicionar/Remover Dispositivo", self)
        self.adicionar_remover_dispositivo_button.clicked.connect(self.mostrar_mensagem_manutencao)
        layout.addWidget(self.adicionar_remover_dispositivo_button)
        self.scanner_rede_button = QPushButton("Iniciar Scanner de Rede", self)
        self.scanner_rede_button.clicked.connect(self.iniciar_scanner_rede)
        layout.addWidget(self.scanner_rede_button)

        self.resultados_scanner_button = QPushButton("Resultados do Scanner de Rede", self)
        self.resultados_scanner_button.clicked.connect(self.mostrar_resultados_scanner)
        layout.addWidget(self.resultados_scanner_button)

        self.historico_eventos_button = QPushButton("Histórico de Eventos", self)
        self.historico_eventos_button.clicked.connect(self.mostrar_mensagem_manutencao)
        layout.addWidget(self.historico_eventos_button)

        self.sair_button = QPushButton("Sair", self)
        self.sair_button.clicked.connect(self.confirmar_saida)
        layout.addWidget(self.sair_button)

        layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(layout)

        self.setStyleSheet(f"background-color: {background_color}; color: {font_color};")

    def mostrar_tabela_computadores(self):
        self.janela_tabela_computadores = JanelaTabelaComputadores()
        self.janela_tabela_computadores.show()

    def iniciar_scanner_rede(self):
        self.janela_scanner_rede = JanelaScannerRede()
        self.janela_scanner_rede.show()

    def mostrar_resultados_scanner(self):
        self.janela_resultados_scanner = JanelaResultadosScanner()
        self.janela_resultados_scanner.show()

    def mostrar_mensagem_manutencao(self):
        QMessageBox.information(self, "Manutenção", "Esta funcionalidade está em manutenção. Por favor, tente novamente mais tarde.")

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

    def mostrar_janela_adicionar_remover_dispositivo(self):
        self.janela_adicionar_remover_dispositivo = JanelaAdicionarRemoverDispositivo()
        self.janela_adicionar_remover_dispositivo.show()
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

        self.setStyleSheet(f"background-color: {background_color}; color: {font_color};")

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

        self.setStyleSheet(f"background-color: {background_color}; color: {font_color};")

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

# Fim da Janela de Tabela de Computadores
class JanelaTabelaComputadores(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista de Computadores")
        self.setFixedSize(600, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.lista_computadores = QListWidget(self)
        layout.addWidget(self.lista_computadores)

        self.carregar_dados()

        self.selecionar_button = QPushButton("Selecionar", self)
        self.selecionar_button.clicked.connect(self.selecionar_computador)
        layout.addWidget(self.selecionar_button)

        self.voltar_button = QPushButton("Voltar", self)
        self.voltar_button.clicked.connect(self.voltar_janela_principal)
        layout.addWidget(self.voltar_button)

        layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(layout)

        self.setStyleSheet(f"background-color: {background_color}; color: {font_color};")

    def carregar_dados(self):
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, ip, porta, opcoes, usuario FROM computadores")
            registros = cursor.fetchall()

        for registro in registros:
            item_text = f"ID: {registro[0]}, IP: {registro[1]}, Porta: {registro[2]}, Opções: {registro[3]}, Usuário: {registro[4]}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, registro[0])  # Store the ID for later use
            self.lista_computadores.addItem(item)

    def selecionar_computador(self):
        selected_item = self.lista_computadores.currentItem()
        if selected_item:
            computador_id = selected_item.data(Qt.UserRole)
            self.carregar_detalhes_computador(computador_id)

    def carregar_detalhes_computador(self, computador_id):
        self.janela_executar_comando = JanelaExecutarComando(computador_id)
        self.janela_executar_comando.show()

    def voltar_janela_principal(self):
        self.close()

# Fim da Janela de Tabela de Computadores
class JanelaAdicionarRemoverDispositivo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adicionar/Remover Dispositivo")
        self.setFixedSize(400, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.ip_label = QLabel("IP do Host:", self)
        layout.addWidget(self.ip_label)
        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText("IP do Host")
        layout.addWidget(self.ip_input)

        self.porta_label = QLabel("Porta:", self)
        layout.addWidget(self.porta_label)
        self.porta_input = QLineEdit(self)
        self.porta_input.setPlaceholderText("Porta")
        layout.addWidget(self.porta_input)

        self.opcoes_label = QLabel("Opções:", self)
        layout.addWidget(self.opcoes_label)
        self.opcoes_input = QLineEdit(self)
        self.opcoes_input.setPlaceholderText("Opções")
        layout.addWidget(self.opcoes_input)

        self.usuario_label = QLabel("Usuário:", self)
        layout.addWidget(self.usuario_label)
        self.usuario_input = QLineEdit(self)
        self.usuario_input.setPlaceholderText("Usuário")
        layout.addWidget(self.usuario_input)

        self.senha_label = QLabel("Senha:", self)
        layout.addWidget(self.senha_label)
        self.senha_input = QLineEdit(self)
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.senha_input)

        self.adicionar_button = QPushButton("Adicionar", self)
        self.adicionar_button.clicked.connect(self.adicionar_dispositivo)
        layout.addWidget(self.adicionar_button)

        self.remover_button = QPushButton("Remover", self)
        self.remover_button.clicked.connect(self.remover_dispositivo)
        layout.addWidget(self.remover_button)

        self.central_widget.setLayout(layout)

        self.setStyleSheet(f"background-color: {background_color}; color: {font_color};")

    def adicionar_dispositivo(self):
        ip = self.ip_input.text()
        porta = self.porta_input.text()
        opcoes = self.opcoes_input.text()
        usuario = self.usuario_input.text()
        senha = self.senha_input.text()

        computador = Computador(ip, porta, opcoes, usuario, senha, 1)  # Assuming usuario_id is 1 for now
        computador.adicionar()

        QMessageBox.information(self, "Sucesso", "Dispositivo adicionado com sucesso")

    def remover_dispositivo(self):
        ip = self.ip_input.text()

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM computadores WHERE ip=?", (ip,))
            conn.commit()

        QMessageBox.information(self, "Sucesso", "Dispositivo removido com sucesso")

class JanelaExecutarComando(QMainWindow):
    def __init__(self, computador_id):
        super().__init__()
        self.setWindowTitle("Executar Comando")
        self.setFixedSize(400, 300)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.computador_id = computador_id

        layout = QVBoxLayout()

        self.button_bitlocker = QPushButton("Gerenciar Bitlocker", self)
        self.button_bitlocker.clicked.connect(self.executar_comando)
        layout.addWidget(self.button_bitlocker)

        self.button_acesso_remoto = QPushButton("Acesso Remoto", self)
        self.button_acesso_remoto.clicked.connect(self.acesso_remoto)
        layout.addWidget(self.button_acesso_remoto)

        self.button_localizar_dispositivo = QPushButton("Localizar Dispositivo", self)
        layout.addWidget(self.button_localizar_dispositivo)

        self.voltar_button = QPushButton("Voltar", self)
        self.voltar_button.clicked.connect(self.voltar_janela_principal)
        layout.addWidget(self.voltar_button)

        self.central_widget.setLayout(layout)
        self.setStyleSheet(f"background-color: {background_color}; color: {font_color};")

    def voltar_janela_principal(self):
        self.close()
        self.janela_principal = JanelaPrincipal()
        self.janela_principal.show()

    def acesso_remoto(self):
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ip FROM computadores WHERE id=?", (self.computador_id,))
            computador = cursor.fetchone()

        if computador:
            ip = computador[0]
            comando_rdp = f'mstsc /v:{ip}'
            resultado = os.system(comando_rdp)
            if resultado != 0:
                QMessageBox.critical(self, "Erro", "Falha ao tentar acessar o computador remotamente")
                self.show()
        else:
            QMessageBox.critical(self, "Erro", "Computador não encontrado")
            self.show()
    
    def executar_comando(self):
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ip, porta, opcoes, usuario, senha, usuario_id FROM computadores WHERE id=?", (self.computador_id,))
            computador = cursor.fetchone()

        if computador:
            ip, porta, opcoes, usuario, senha, usuario_id = computador
            comp = Computador(ip, porta, opcoes, usuario, senha, usuario_id)
            resultado = comp.verificar_bitlocker()
            if resultado:
                QMessageBox.information(self, "Sucesso", f"Status do BitLocker:\n{resultado}")
            else:
                QMessageBox.critical(self, "Erro", "Erro ao verificar o status do BitLocker")
        else:
            QMessageBox.critical(self, "Erro", "Computador não encontrado")

class JanelaScannerRede(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scanner de Rede")
        self.setFixedSize(600, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.resultados_text = QLabel("Resultados do Scanner de Rede:", self)
        layout.addWidget(self.resultados_text)

        self.resultados_lista = QListWidget(self)
        layout.addWidget(self.resultados_lista)

        self.iniciar_scanner_button = QPushButton("Iniciar Scanner", self)
        self.iniciar_scanner_button.clicked.connect(self.iniciar_scanner)
        layout.addWidget(self.iniciar_scanner_button)

        self.voltar_button = QPushButton("Voltar", self)
        self.voltar_button.clicked.connect(self.voltar_janela_principal)
        layout.addWidget(self.voltar_button)

        self.central_widget.setLayout(layout)
        self.setStyleSheet(f"background-color: {background_color}; color: {font_color};")

    def iniciar_scanner(self):
        self.scanner_rede = ScannerRede()
        resultados = self.scanner_rede.escanear()
        if resultados:
            self.resultados_lista.clear()
            for resultado in resultados:
                item_text = f"Hostname: {resultado[0]}, MAC: {resultado[1]}, IP: {resultado[2]}, Portas: {resultado[3]}"
                self.resultados_lista.addItem(QListWidgetItem(item_text))
            QMessageBox.information(self, "Sucesso", "Escaneamento de rede concluído com sucesso")
        else:
            QMessageBox.critical(self, "Erro", "Erro ao escanear a rede")

    def voltar_janela_principal(self):
        self.close()
        self.janela_principal = JanelaPrincipal()

class ScannerRede:
    def __init__(self, portas_selecionadas=None):
        self.portas_selecionadas = portas_selecionadas if portas_selecionadas else ['80', '22', '443']
        self.escaneamento_concluido = False

    def escanear(self):
        ip = socket.gethostbyname(socket.gethostname())
        mascara = ipaddress.IPv4Network(f"{ip}/24", strict=False).netmask
        rede = ipaddress.IPv4Network(f"{ip}/{mascara}", strict=False)

        argumentos = []
        if self.portas_selecionadas:
            portas = ','.join(self.portas_selecionadas)
            argumentos.append(f'-p {portas}')

        argumentos_str = ' '.join(argumentos)

        nm = nmap.PortScanner()
        try:
            nm.scan(hosts=str(rede), arguments=argumentos_str)

            resultados = []
            for host in nm.all_hosts():
                nome_host = nm[host].hostname() if nm[host].hostname() else 'N/A'
                endereco_mac = nm[host]['addresses'].get('mac', 'N/A')
                endereco_ip = nm[host]['addresses'].get('ipv4', 'N/A')
                portas_abertas = ', '.join([
                    f"{port}/ABERTA" if port.isdigit() and nm[host].has_tcp(int(port)) and 'tcp' in nm[host] and int(port) in nm[host]['tcp'] and nm[host]['tcp'][int(port)]['state'] == 'open' 
                    else f"{port}/FECHADA" 
                    for port in self.portas_selecionadas
                ])
                if not portas_abertas:
                    portas_abertas = 'N/D'
                resultados.append((nome_host, endereco_mac, endereco_ip, portas_abertas))

            self.salvar_resultados(resultados)
            self.escaneamento_concluido = True
            return resultados
        except Exception as e:
            print(f"Erro ao executar o comando nmap: {e}")
            self.escaneamento_concluido = False
            return None

    def salvar_resultados(self, resultados):
        try:
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                for resultado in resultados:
                    cursor.execute('''
                        INSERT INTO scanner (usuario_id, data, hostname, mac_address, ip, portas)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), resultado[0], resultado[1], resultado[2], resultado[3]))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao salvar resultados: {e}")

    def obter_informacoes(self):
        try:
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM scanner')
                resultados = cursor.fetchall()
                return resultados
        except sqlite3.Error as e:
            print(f"Erro ao obter informações: {e}")
            return None

class RedeAtual:
    def __init__(self):
        pass

    def obter_rede_atual(self):
        try:
            ip = socket.gethostbyname(socket.gethostname())
            mascara = ipaddress.IPv4Network(f"{ip}/24", strict=False).netmask
            rede = ipaddress.IPv4Network(f"{ip}/{mascara}", strict=False)
            return str(rede)
        except Exception as e:
            print(f"Erro ao obter a rede atual: {e}")
            return None

class JanelaResultadosScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resultados do Scanner de Rede")
        self.setFixedSize(600, 400)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.resultados_tabela = QTableWidget(self)
        self.resultados_tabela.setColumnCount(6)
        self.resultados_tabela.setHorizontalHeaderLabels(["ID", "Usuário ID", "Data", "Hostname", "MAC Address", "IP", "Portas"])
        layout.addWidget(self.resultados_tabela)

        self.carregar_dados()

        self.voltar_button = QPushButton("Voltar", self)
        self.voltar_button.clicked.connect(self.voltar_janela_principal)
        layout.addWidget(self.voltar_button)

        self.central_widget.setLayout(layout)
        self.setStyleSheet(f"background-color: {background_color}; color: {font_color};")

    def carregar_dados(self):
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scanner")
            registros = cursor.fetchall()

        self.resultados_tabela.setRowCount(len(registros))
        for row_idx, registro in enumerate(registros):
            for col_idx, valor in enumerate(registro):
                self.resultados_tabela.setItem(row_idx, col_idx, QTableWidgetItem(str(valor)))

    def voltar_janela_principal(self):
        self.close()
        self.janela_principal = JanelaPrincipal()
        self.janela_principal.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tela_carregamento = TelaCarregamento()
    tela_carregamento.show()
    sys.exit(app.exec_())
