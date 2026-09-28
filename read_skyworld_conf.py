import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/files/contents', headers=h, params={'file': 'plugins/BlueMap/maps/skyworld.conf'})
print(r.text[:300])
