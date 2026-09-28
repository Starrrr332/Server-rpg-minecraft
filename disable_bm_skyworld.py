import requests
import json

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
payload = {
    'root': '/plugins/BlueMap/maps',
    'files': [
        {'from': 'skyworld.conf', 'to': 'skyworld.conf.disabled'},
        {'from': 'skyworld_nether.conf', 'to': 'skyworld_nether.conf.disabled'}
    ]
}
r = requests.put(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/files/rename', headers=h, json=payload)
print("Status rename:", r.status_code)

# Enviar recarga suave de BlueMap
if r.status_code in [200, 204]:
    print("Mapas deshabilitados exitosamente. Enviando /bluemap reload...")
    requests.post(f'{cfg["panel_url"]}/api/client/servers/{cfg["server_id"]}/command', headers=h, json={'command': 'bluemap reload'})
    print("Orden enviada.")
