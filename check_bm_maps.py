import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/files/list?directory=plugins/BlueMap/maps', headers=h)
print("Status:", r.status_code)
if r.status_code == 200:
    for it in r.json()['data']:
        print("  Map file:", it['attributes']['name'])
