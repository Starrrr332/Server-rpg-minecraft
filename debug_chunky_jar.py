# -*- coding: utf-8 -*-
import json
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

print("=== VERIFICANDO ARCHIVOS EN /plugins ===")
r = requests.get(f"{base_url}/files/list", headers=headers, params={"directory": "/plugins"}, timeout=10)
if r.status_code == 200:
    items = r.json().get('data', [])
    names = [item['attributes']['name'] for item in items]
    chunky_files = [n for n in names if 'chunky' in n.lower()]
    print("Archivos de Chunky en /plugins:", chunky_files)

print("\n=== BUSCANDO MENSAJES DE CHUNKY EN LATEST.LOG DE ARRANQUE ===")
r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={"file": "logs/latest.log"}, timeout=10)
if r_log.status_code == 200:
    lines = r_log.text.splitlines()
    chunky_lines = [l for l in lines if 'chunky' in l.lower() or 'loading' in l.lower() or 'enable' in l.lower()]
    print(f"Total líneas encontradas: {len(chunky_lines)}")
    for cl in chunky_lines[:25]:
        print(" ", cl.encode('ascii', errors='replace').decode('ascii'))
