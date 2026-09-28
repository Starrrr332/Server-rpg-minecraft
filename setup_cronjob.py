import subprocess
import os

def setup_cron():
    bat_path = os.path.abspath('actualizar_y_subir.bat')
    # Schtasks command
    cmd = [
        'schtasks', '/create',
        '/tn', 'HolyServer_StatsSync',
        '/tr', f'"{bat_path}"',
        '/sc', 'MINUTE',
        '/mo', '30',
        '/f'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Return code:", res.returncode)
    if res.stdout:
        print("Output:", res.stdout.strip())
    if res.stderr:
        print("Error:", res.stderr.strip())

if __name__ == '__main__':
    setup_cron()
