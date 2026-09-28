import requests
import json
import time

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
base_url = f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}"

r = requests.post(f"{base_url}/command", headers=h, json={'command': 'minecraft:give mocosupremo777 elytra 1'}, timeout=5)
print(f"Comando enviado: {r.status_code}")
time.sleep(1)

r_log = requests.get(f"{base_url}/files/contents", headers=h, params={'file': 'logs/latest.log'}, timeout=10)
if r_log.status_code == 200:
    print("Últimas líneas del log:")
    for l in r_log.text.splitlines()[-6:]:
        print(" ", l)
