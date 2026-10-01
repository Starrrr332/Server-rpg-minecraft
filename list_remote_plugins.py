import requests
import json

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

r = requests.get(f"{base_url}/files/list", headers=headers, params={'directory': '/plugins'}, timeout=10)
if r.status_code == 200:
    items = r.json().get('data', [])
    print(f"Total items in /plugins: {len(items)}")
    for item in items:
        name = item['attributes']['name']
        print(" -", name)
else:
    print("Error listing /plugins:", r.status_code)
