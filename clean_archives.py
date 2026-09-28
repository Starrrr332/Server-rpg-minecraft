import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/files/list', headers=h)
archives = [it['attributes']['name'] for it in r.json().get('data', []) if it['attributes']['name'].endswith('.tar.gz')]
print('Archives in server root:', archives)
if archives:
    del_r = requests.post(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/files/delete', headers=h, json={'root': '/', 'files': archives})
    print('Cleaned up server archives:', del_r.status_code)
