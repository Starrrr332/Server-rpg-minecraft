import json
import requests

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}"}

r = requests.get(f"{base_url}/files/list", headers=headers, params={"directory": "/plugins"})
if r.status_code == 200:
    files = r.json().get("data", [])
    for f in files:
        attr = f.get("attributes", {})
        print(f"{attr.get('name')} - {attr.get('size')} bytes")
else:
    print(r.status_code, r.text)
