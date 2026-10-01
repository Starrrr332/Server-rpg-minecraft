import requests
import json

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

r = requests.get(f"{base_url}/files/list", headers=headers, params={'directory': '/plugins/EliteMobs/customquests'}, timeout=10)
if r.status_code == 200:
    items = [item['attributes']['name'] for item in r.json().get('data', [])]
    print(f"Total custom quests found: {len(items)}")
    for item in items:
        print(" -", item)
else:
    print("Error listing customquests:", r.status_code)
