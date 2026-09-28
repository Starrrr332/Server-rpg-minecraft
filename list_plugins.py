import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/files/list?directory=plugins', headers=h)
if r.status_code == 200:
    jars = []
    dirs = []
    for it in r.json()['data']:
        name = it['attributes']['name']
        size = it['attributes']['size']
        if it['attributes']['is_file'] and name.endswith('.jar'):
            jars.append((name, size))
        elif not it['attributes']['is_file']:
            dirs.append(name)
    print(f"Total plugins jar: {len(jars)}")
    for name, size in sorted(jars):
        print(f"  {name:45} ({size / (1024*1024):.2f} MB)")
    print(f"\nDirectorios en plugins: {len(dirs)}")
    print(", ".join(dirs[:20]))
else:
    print("Error:", r.status_code)
