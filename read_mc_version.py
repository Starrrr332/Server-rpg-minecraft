import requests
import json

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
if r_log.status_code == 200:
    for line in r_log.text.splitlines()[:50]:
        print(line)
