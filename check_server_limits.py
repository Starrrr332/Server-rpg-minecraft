import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}', headers=h)
print("Status:", r.status_code)
if r.status_code == 200:
    attr = r.json()['attributes']
    print("Limits:", attr.get('limits'))
    print("Feature limits:", attr.get('feature_limits'))
