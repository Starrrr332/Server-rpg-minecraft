import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/files/contents', headers=h, params={'file': 'logs/latest.log'})
bm_lines = [l for l in r.text.splitlines() if 'BlueMap' in l or 'bluemap' in l]
print(f"Total BlueMap log lines: {len(bm_lines)}")
for l in bm_lines[-15:]:
    print(l)
