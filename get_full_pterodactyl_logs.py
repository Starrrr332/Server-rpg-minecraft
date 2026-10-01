import json
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}"}

r = requests.get(f"{base_url}/files/contents", headers=headers, params={"file": "logs/latest.log"})
if r.status_code == 200:
    lines = r.text.splitlines()
    print(f"Total lineas en logs/latest.log: {len(lines)}")
    print("--- ULTIMAS 25 LINEAS DE LOGS/LATEST.LOG ---")
    for line in lines[-25:]:
        print(line)
else:
    print("Error leyendo logs/latest.log:", r.status_code, r.text)
