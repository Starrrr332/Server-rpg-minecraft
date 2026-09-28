import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
for file in ['bukkit.yml', 'spigot.yml', 'server.properties']:
    r = requests.get(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/files/contents', headers=h, params={'file': file})
    print(f"=== {file} ===")
    for line in r.text.splitlines():
        if any(k in line for k in ['view-distance', 'simulation-distance', 'ticks-per', 'spawn-limits', 'chunk', 'entity-tracking-range', 'max-tick-time', 'network-compression']):
            print(" ", line)
