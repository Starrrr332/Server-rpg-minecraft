import os
import sys
import time
import json
import datetime
import requests
from google_drive_manager import GoogleDriveManager

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bot_config.json')
BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
STATUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sentinel_status.json')
os.makedirs(BACKUP_DIR, exist_ok=True)

class ServerSentinel:
    def __init__(self):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            self.cfg = json.load(f)
        self.headers = {
            'Authorization': f"Bearer {self.cfg['api_key']}",
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolySentinel/1.0'
        }
        self.base_url = f"{self.cfg['panel_url']}/api/client/servers/{self.cfg['server_id']}"
        self.ram_limit_mb = 8192.0
        self.drive_mgr = GoogleDriveManager()

    # ==========================================
    # 1. MONITOREO Y OPTIMIZACIÓN DE MEMORIA
    # ==========================================
    def get_resources(self):
        """Consulta los recursos en tiempo real del servidor."""
        try:
            r = requests.get(f"{self.base_url}/resources", headers=self.headers, timeout=10)
            if r.status_code == 200:
                data = r.json()['attributes']
                res = data.get('resources', {})
                state = data.get('current_state', 'unknown')
                cpu = res.get('cpu_absolute', 0.0)
                mem_bytes = res.get('memory_bytes', 0)
                mem_mb = mem_bytes / (1024 * 1024)
                disk_mb = res.get('disk_bytes', 0) / (1024 * 1024)
                uptime_sec = res.get('uptime', 0) / 1000
                ram_percent = (mem_mb / self.ram_limit_mb) * 100.0

                status = {
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'state': state,
                    'cpu_percent': round(cpu, 2),
                    'ram_mb': round(mem_mb, 1),
                    'ram_percent': round(ram_percent, 1),
                    'ram_limit_mb': self.ram_limit_mb,
                    'disk_mb': round(disk_mb, 1),
                    'uptime_seconds': int(uptime_sec)
                }

                # Guardar estado para mando de control
                with open(STATUS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(status, f, indent=2)

                return status
        except Exception as e:
            print(f"[Sentinel Error] Error obteniendo recursos: {e}")
        return None

    def trigger_soft_memory_cleanup(self):
        """Aplica un alivio suave de memoria sin reiniciar ni expulsar jugadores."""
        print("[Sentinel Optimización] Ejecutando purga preventiva de memoria no utilizada...")
        try:
            # 1. Guardar cambios en disco
            requests.post(f"{self.base_url}/command", headers=self.headers, json={'command': 'save-all'}, timeout=5)
            # 2. Limpieza de items huérfanos con ClearLag (comando real: /clearlag)
            requests.post(f"{self.base_url}/command", headers=self.headers, json={'command': 'clearlag clear items'}, timeout=5)
            print("[Sentinel Optimización] Comandos /save-all y /clearlag clear items enviados con éxito.", flush=True)
            return True
        except Exception as e:
            print(f"[Sentinel Optimización Error] {e}")
            return False

    def run_monitor_loop(self, interval_seconds=60):
        """Ciclo continuo de monitoreo del servidor."""
        print(f"=== CENTINELA INICIADO (Intervalo: {interval_seconds}s) ===")
        print(f"Límite de RAM vigilado: {self.ram_limit_mb} MB")

        while True:
            status = self.get_resources()
            if status:
                now_str = status['timestamp']
                ram = status['ram_mb']
                pct = status['ram_percent']
                cpu = status['cpu_percent']

                # Determinar nivel de alerta
                if pct >= 88.0:
                    alert = "[CRITICO]"
                    # Accionar purga si la memoria está asfixiando el servidor
                    self.trigger_soft_memory_cleanup()
                elif pct >= 78.0:
                    alert = "[PRECAUCION]"
                else:
                    alert = "[OPTIMO]"

                print(f"[{now_str}] {alert} RAM: {ram:.1f}MB ({pct:.1f}%) | CPU: {cpu:.1f}% | Estado: {status['state']}", flush=True)

            time.sleep(interval_seconds)

    # ==========================================
    # 2. MANDO DE CONTROL DE ARCHIVOS
    # ==========================================
    def list_files(self, directory=""):
        """Lista archivos y carpetas dentro del servidor."""
        url = f"{self.base_url}/files/list"
        params = {'directory': directory} if directory else {}
        r = requests.get(url, headers=self.headers, params=params, timeout=10)
        if r.status_code == 200:
            items = []
            for it in r.json().get('data', []):
                attr = it['attributes']
                items.append({
                    'name': attr['name'],
                    'is_file': attr['is_file'],
                    'size': attr['size'],
                    'modified': attr.get('modified_at')
                })
            return items
        return []

    def read_file(self, filepath):
        """Lee el contenido de un archivo de texto en el servidor."""
        r = requests.get(f"{self.base_url}/files/contents", headers=self.headers, params={'file': filepath}, timeout=15)
        if r.status_code == 200:
            return r.text
        return None

    def write_file(self, filepath, content):
        """Escribe o actualiza un archivo de configuración en el servidor."""
        # Se usa el endpoint write
        headers = dict(self.headers)
        headers['Content-Type'] = 'text/plain'
        r = requests.post(f"{self.base_url}/files/write", headers=headers, params={'file': filepath}, data=content.encode('utf-8'), timeout=15)
        return r.status_code in [200, 204]

    # ==========================================
    # 3. SISTEMA DE COPIAS DE SEGURIDAD (DRIVE)
    # ==========================================
    def perform_backup_and_upload(self, targets=['world', 'plugins', 'server.properties', 'bukkit.yml', 'spigot.yml']):
        """Comprime carpetas críticas en el servidor, descarga la copia y la sube a Google Drive."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n=== INICIANDO COPIA DE SEGURIDAD ({timestamp}) ===")

        # 1. Guardar estado del juego
        print("[1/5] Ejecutando save-all en el servidor...")
        requests.post(f"{self.base_url}/command", headers=self.headers, json={'command': 'save-all'}, timeout=5)
        time.sleep(2)

        # 2. Comprimir en el host remoto
        print(f"[2/5] Solicitando compresión remota de: {targets}...")
        payload = {
            'root': '/',
            'files': targets
        }
        r_comp = requests.post(f"{self.base_url}/files/compress", headers=self.headers, json=payload, timeout=30)
        if r_comp.status_code != 200:
            print(f"[ERROR] No se pudo iniciar la compresión en el servidor: {r_comp.status_code}")
            return False

        archive_name = r_comp.json()['attributes']['name']
        print(f"  + Archivo comprimido generado en el servidor: {archive_name}")

        # 3. Obtener URL de descarga
        print("[3/5] Obteniendo enlace de descarga del archivo...")
        r_dl = requests.get(f"{self.base_url}/files/download", headers=self.headers, params={'file': archive_name}, timeout=15)
        if r_dl.status_code != 200:
            print(f"[ERROR] No se pudo obtener la URL de descarga: {r_dl.status_code}")
            return False

        download_url = r_dl.json()['attributes']['url']
        local_archive_path = os.path.join(BACKUP_DIR, f"HolyServer_Backup_{timestamp}.tar.gz")

        # 4. Descargar localmente
        print(f"[4/5] Descargando copia a almacenamiento local: {local_archive_path}...")
        with requests.get(download_url, stream=True) as stream_res:
            with open(local_archive_path, 'wb') as f:
                for chunk in stream_res.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        archive_size_mb = os.path.getsize(local_archive_path) / (1024 * 1024)
        print(f"  + Copia descargada exitosamente: {archive_size_mb:.2f} MB")

        # Limpiar archivo temporal del servidor remoto para no saturar el disco del host
        requests.post(f"{self.base_url}/files/delete", headers=self.headers, json={'root': '/', 'files': [archive_name]}, timeout=10)
        print("  + Archivo temporal del servidor eliminado limpiamente.")

        # 5. Subir a Google Drive
        print("[5/5] Sincronizando copia de seguridad con Google Drive...")
        drive_res = self.drive_mgr.upload_file(local_archive_path, max_retention=5)
        if drive_res:
            print("=== COPIA DE SEGURIDAD COMPLETADA Y SUBIDA A GOOGLE DRIVE CON ÉXITO ===")
            return True
        else:
            print("=== COPIA GUARDADA LOCALMENTE (Pendiente sincronización con Drive) ===")
            print(f"Archivo seguro en: {local_archive_path}")
            return False

if __name__ == '__main__':
    sentinel = ServerSentinel()
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd in ['--status', '-s']:
            res = sentinel.get_resources()
            print(json.dumps(res, indent=2))
        elif cmd in ['--clean', '-c']:
            sentinel.trigger_soft_memory_cleanup()
        elif cmd in ['--backup', '-b']:
            sentinel.perform_backup_and_upload()
        elif cmd in ['--monitor', '-m']:
            sentinel.run_monitor_loop(interval_seconds=60)
        else:
            print("Comandos disponibles: --status, --clean, --backup, --monitor")
    else:
        # Default report
        res = sentinel.get_resources()
        print(f"Centinela listo. Estado actual: RAM {res['ram_mb']}MB ({res['ram_percent']}%) | CPU: {res['cpu_percent']}%")
