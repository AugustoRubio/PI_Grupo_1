import sqlite3
from bancodados import db_file, registrar_alteracao
from winrm.protocol import Protocol
import os
# Ensure that JanelaExecutarComando is correctly imported from the right module
try:
    from interface import JanelaExecutarComando
    import subprocess
except ImportError:
    import subprocess
    class JanelaExecutarComando:
        def obter_ip_selecionado(self):
            # Dummy implementation for the purpose of this example
            return '127.0.0.1'

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
    
    def verificar_bitlocker(self):

        comando = 'Get-BitLockerVolume | Select-Object -ExpandProperty VolumeStatus'

        try:
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT usuario, senha
                FROM computadores
                WHERE ip = ?
                ''', (self.ip,))
                result = cursor.fetchone()
                if result:
                    usuario, senha = result
                else:
                    print("Credenciais não encontradas no banco de dados.")
                    return None

            p = Protocol(
                endpoint=f'http://{self.ip}:5985/wsman',
                transport='ntlm',
                username=usuario,
                password=senha
            )
            shell_id = p.open_shell()
            command_id = p.run_command(shell_id, 'powershell.exe', ['-Command', comando])
            std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
            p.cleanup_command(shell_id, command_id)
            p.close_shell(shell_id)

            if status_code == 0:
                return std_out.decode('utf-8').strip()
            else:
                print(f"Error: {std_err.decode('utf-8')}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def conectar_rdp(self):

        janela = JanelaExecutarComando()
        ip_selecionado = janela.obter_ip_selecionado()

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT ip, porta, opcoes, usuario, senha, usuario_id
            FROM computadores
            WHERE ip = ?
            ''', (ip_selecionado,))
            computador = cursor.fetchone()

            if computador:
                ip = computador[0]
                comando_rdp = f'mstsc /v:{ip}'
                os.system(comando_rdp)
            else:
                print("Computador não encontrado no banco de dados.")