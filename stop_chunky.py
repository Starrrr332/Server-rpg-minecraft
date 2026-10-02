# -*- coding: utf-8 -*-
import json
import requests
import time

def main():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json"
    }

    print("[!] Cancelando tarea de Chunky...")
    commands = ["chunky cancel", "chunky quiet 0"]
    for cmd in commands:
        r = requests.post(f"{base_url}/command", headers=headers, json={"command": cmd}, timeout=10)
        print(f"  Enviado '{cmd}': HTTP {r.status_code}")
        time.sleep(1)

    time.sleep(2)

    # Confirmar en logs
    r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        print("\n--- CONSOLE LOGS ---")
        for l in lines[-15:]:
            print(" ", l.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    main()
