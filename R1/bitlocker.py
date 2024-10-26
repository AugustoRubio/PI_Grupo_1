import sys
import subprocess
import ctypes
import os

class BitLockerManager:
    def __init__(self):
        self.status_checked = False

    def check_status(self):
        if self.status_checked:
            return "Status already checked."
        if not self.is_admin():
            return self.elevate_privileges()
        try:
            result = subprocess.run(['manage-bde', '-status'], capture_output=True, text=True)
            self.status_checked = True
            if result.returncode == 0:
                return f"BitLocker Status: {result.stdout}"
            else:
                return f"Failed to check status: {result.stderr}"
        except Exception as e:
            return f"Failed to check status: {e}"

    def enable_bitlocker(self):
        if not self.is_admin():
            return self.elevate_privileges()
        try:
            result = subprocess.run(['manage-bde', '-on', 'C:'], capture_output=True, text=True)
            if result.returncode == 0:
                return "BitLocker enabled successfully."
            else:
                return f"Failed to enable BitLocker: {result.stderr}"
        except Exception as e:
            return f"Failed to enable BitLocker: {e}"

    def disable_bitlocker(self):
        if not self.is_admin():
            return self.elevate_privileges()
        try:
            result = subprocess.run(['manage-bde', '-off', 'C:'], capture_output=True, text=True)
            if result.returncode == 0:
                return "BitLocker disabled successfully."
            else:
                return f"Failed to disable BitLocker: {result.stderr}"
        except Exception as e:
            return f"Failed to disable BitLocker: {e}"

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def elevate_privileges(self):
        if ctypes.windll.shell32.IsUserAnAdmin():
            return
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        print("Privileges elevated. Please run the script again.")
        sys.exit()

    def close_privilege_windows(self):
        if self.is_admin():
            try:
                os.system("taskkill /F /IM consent.exe")
                return "Privilege windows closed."
            except Exception as e:
                return f"Failed to close privilege windows: {e}"
        else:
            return "No admin privileges to close windows."

    def hide_console_window(self):
        if self.is_admin():
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

if __name__ == "__main__":
    manager = BitLockerManager()
    manager.hide_console_window()
    print(manager.check_status())
    print(manager.enable_bitlocker())
    print(manager.disable_bitlocker())
    print(manager.close_privilege_windows())
