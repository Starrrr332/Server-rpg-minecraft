import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/backups', headers=h)
print("Backups endpoint status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    print("Backups count:", len(data.get('data', [])))
    for b in data.get('data', []):
        attr = b['attributes']
        print(f"  Backup: {attr.get('name')} | Size: {attr.get('bytes') / (1024*1024):.1f} MB | Completed: {attr.get('is_successful')}")
else:
    print(r.text[:200])
