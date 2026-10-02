import json
import requests
import time
import re

def start_chunky():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json"
    }

    print("==================================================")
    print(">> INICIANDO PRE-GENERACION CON CHUNKY (WORLD)")
    print("==================================================")

    # List of setup commands
    commands = [
        "chunky quiet 10",         # Notificaciones cada 10 segundos
        "chunky world world",      # Seleccionar mundo principal
        "chunky center 0 0",       # Centro en (0, 0)
        "chunky shape circle",     # Forma circular
        "chunky radius 4000",      # Radio de 4,000 bloques (~250 chunks)
        "chunky start"             # Iniciar tarea
    ]

    for cmd in commands:
        print(f"  [CONSOLA] > {cmd}")
        requests.post(f"{base_url}/command", headers=headers, json={'command': cmd}, timeout=10)
        time.sleep(1.5)

    print("\nEsperando 5 segundos para recibir telemetria del log...")
    time.sleep(5)

    # Check log for Chunky task output
    r_log = requests.get(f"{base_url}/files/contents", headers={"Authorization": f"Bearer {cfg['api_key']}"}, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        chunky_lines = [l for l in lines[-30:] if 'chunky' in l.lower() or 'task' in l.lower()]
        print("\n--- ULTIMOS LOGS DE CHUNKY ---")
        for l in chunky_lines[-10:]:
            print("  ", l.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    start_chunky()
