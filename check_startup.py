import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

headers = {
    'Authorization': f'Bearer {cfg["api_key"]}',
    'Accept': 'application/json'
}

r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/startup', headers=headers)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Startup command:", data.get('meta', {}).get('raw_startup_command'))
    for v in data.get('data', []):
        attr = v['attributes']
        print(f"{attr['env_variable']} = {attr['server_value']}")
else:
    print(r.text[:200])
