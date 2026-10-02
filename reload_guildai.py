import json
import requests
import time

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {
    "Authorization": f"Bearer {cfg['api_key']}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

r = requests.post(f"{base_url}/command", headers=headers, json={"command": "guildai reload"}, timeout=10)
print("Respuesta comando /guildai reload:", r.status_code)

time.sleep(1)

r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
if r_log.status_code == 200:
    lines = r_log.text.splitlines()
    print("\n--- ULTIMAS 10 LINEAS DE LOG ---")
    for l in lines[-10:]:
        print(l.encode('ascii', errors='replace').decode('ascii'))
