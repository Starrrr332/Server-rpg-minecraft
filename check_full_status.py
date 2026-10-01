import requests
import json

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

r_res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
if r_res.status_code == 200:
    st = r_res.json().get('attributes', {}).get('current_state')
    print(f"Estado Pterodactyl: {st}")
else:
    print(f"Error obteniendo recursos: {r_res.status_code}")

r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
if r_log.status_code == 200:
    lines = r_log.text.splitlines()
    print(f"\n--- ÚLTIMAS 20 LÍNEAS DE LOGS/LATEST.LOG (Total {len(lines)}) ---")
    for line in lines[-20:]:
        print(line)
else:
    print(f"Error obteniendo logs: {r_log.status_code}")
