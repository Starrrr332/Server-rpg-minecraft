import requests
import json

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"})

def list_dir(p):
    r = session.get(f"{base_url}/files/list", params={'directory': p}, timeout=10)
    if r.status_code == 200:
        return [item['attributes']['name'] for item in r.json().get('data', [])]
    return []

npc_files = list_dir("/plugins/EliteMobs/npcs")
print(f"Encontrados {len(npc_files)} archivos en /plugins/EliteMobs/npcs/\n")

teleporters = [f for f in npc_files if "teleport" in f.lower() or "vigia" in f.lower() or "maestro" in f.lower()]
for f in teleporters:
    r = session.get(f"{base_url}/files/contents", params={'file': f"/plugins/EliteMobs/npcs/{f}"}, timeout=10)
    if r.status_code == 200:
        text = r.text
        name = ""
        loc = ""
        dung = ""
        for line in text.splitlines():
            if line.startswith("name:"): name = line.strip()
            if "teleportlocation" in line.lower() or "spawnlocation" in line.lower(): loc += line.strip() + " "
            if "dungeon" in line.lower(): dung += line.strip() + " "
        print(f"[{f:35s}] | {name:30s} | {loc[:50]} | {dung[:40]}")
