import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/startup', headers=h)
if r.status_code == 200:
    for it in r.json().get('data', []):
        attr = it['attributes']
        print(f"Env: {attr.get('env_variable')} | Name: {attr.get('name')} | Value: {attr.get('server_value')} | Editable: {attr.get('is_editable')}")
