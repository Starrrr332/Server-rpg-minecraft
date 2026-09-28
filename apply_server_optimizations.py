import requests
import json
import re

with open('bot_config.json') as f:
    cfg = json.load(f)

h = {'Authorization': f'Bearer {cfg["api_key"]}', 'Accept': 'application/json'}
base_url = f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}"

def write_file(path, content):
    headers = dict(h)
    headers['Content-Type'] = 'text/plain'
    r = requests.post(f"{base_url}/files/write", headers=headers, params={'file': path}, data=content.encode('utf-8'), timeout=15)
    print(f"Write {path}: {r.status_code}")
    return r.status_code in [200, 204]

def get_file(path):
    r = requests.get(f"{base_url}/files/contents", headers=h, params={'file': path}, timeout=15)
    return r.text if r.status_code == 200 else None

print("=== OPTIMIZANDO ARCHIVOS DE CONFIGURACIÓN DEL SERVIDOR ===")

# 1. Optimizar server.properties
props = get_file('server.properties')
if props:
    props = re.sub(r'view-distance=\d+', 'view-distance=6', props)
    props = re.sub(r'simulation-distance=\d+', 'simulation-distance=4', props)
    write_file('server.properties', props)
    print("  + server.properties optimizado: view-distance=6, simulation-distance=4")

# 2. Optimizar bukkit.yml
bukkit = get_file('bukkit.yml')
if bukkit:
    bukkit = re.sub(r'period-in-ticks:\s*\d+', 'period-in-ticks: 300', bukkit)
    bukkit = re.sub(r'monsters:\s*\d+', 'monsters: 35', bukkit)
    bukkit = re.sub(r'animals:\s*\d+', 'animals: 6', bukkit)
    write_file('bukkit.yml', bukkit)
    print("  + bukkit.yml optimizado: chunk-gc=300 ticks, spawn-limits ajustados")

# 3. Optimizar spigot.yml
spigot = get_file('spigot.yml')
if spigot:
    spigot = re.sub(r'unload-frozen-chunks:\s*false', 'unload-frozen-chunks: true', spigot)
    spigot = re.sub(r'item-despawn-rate:\s*\d+', 'item-despawn-rate: 2400', spigot)
    spigot = re.sub(r'arrow-despawn-rate:\s*\d+', 'arrow-despawn-rate: 600', spigot)
    write_file('spigot.yml', spigot)
    print("  + spigot.yml optimizado: unload-frozen-chunks=true, item-despawn-rate=2400")

# Ejecutar save-all y purga de items huerfanos inmediata con ClearLag
requests.post(f"{base_url}/command", headers=h, json={'command': 'save-all'}, timeout=5)
requests.post(f"{base_url}/command", headers=h, json={'command': 'lagg clear'}, timeout=5)
requests.post(f"{base_url}/command", headers=h, json={'command': 'lagg unloadchunks'}, timeout=5)
print("  + Purgas suaves ejecutadas en el servidor.")
