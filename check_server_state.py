import json
import requests

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}"}

r = requests.get(f"{base_url}/resources", headers=headers)
if r.status_code == 200:
    print("Server state:", r.json().get('attributes', {}).get('current_state'))
