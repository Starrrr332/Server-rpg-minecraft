# -*- coding: utf-8 -*-
import json
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
if r_log.status_code == 200:
    lines = r_log.text.splitlines()
    chunky_lines = [l for l in lines if '[chunky]' in l.lower()]
    print(f"Total líneas de Chunky registradas: {len(chunky_lines)}")
    print("\n--- ÚLTIMOS REPORTES DE PROGRESO DE CHUNKY ---")
    for cl in chunky_lines[-15:]:
        print(" ", cl.encode('ascii', errors='replace').decode('ascii'))
