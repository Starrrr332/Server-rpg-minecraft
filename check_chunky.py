import requests
import json

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

r = requests.get(f"{base_url}/files/list", headers=headers, params={'directory': '/plugins'}, timeout=10)
if r.status_code == 200:
    items = [item['attributes']['name'] for item in r.json().get('data', [])]
    chunky_items = [i for i in items if "chunky" in i.lower()]
    print("Elementos Chunky encontrados:", chunky_items)
    print("\nTotal plugins:", len(items))
else:
    print("Error listing /plugins:", r.status_code)
