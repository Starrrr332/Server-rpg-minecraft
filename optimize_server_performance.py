import requests
import json
import re
import time

def optimize_all():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    def read_file(path):
        r = requests.get(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
            headers=headers,
            params={'file': path},
            timeout=15
        )
        return r.text if r.status_code == 200 else None

    def write_file(path, content):
        url = f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/write?file={path}"
        r = requests.post(
            url,
            headers={**headers, 'Content-Type': 'application/octet-stream'},
            data=content.encode('utf-8'),
            timeout=20
        )
        return r.status_code in [200, 204]

    # --- 1. Pausar BlueMap render inmediatamente en consola ---
    print("1. Pausando render intensivo de BlueMap en la consola...")
    requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/command",
        headers=headers,
        json={'command': 'bluemap pause'},
        timeout=10
    )

    # --- 2. Optimizar BlueMap core.conf & plugin.conf ---
    print("2. Configurando BlueMap para bajo consumo y pausa con jugadores...")
    core = read_file('/plugins/BlueMap/core.conf')
    if core:
        core = re.sub(r'render-thread-count:\s*\d+', 'render-thread-count: 1', core)
        core = core.replace('#render-thread-priority: 1', 'render-thread-priority: 1')
        if 'render-thread-priority: 1' not in core:
            core = core.replace('render-thread-count: 1', 'render-thread-count: 1\nrender-thread-priority: 1')
        write_file('/plugins/BlueMap/core.conf', core)
        print("  [OK] core.conf optimizado")

    plugin = read_file('/plugins/BlueMap/plugin.conf')
    if plugin:
        # Pausa automatica de renders si hay 1 o mas jugadores online
        plugin = re.sub(r'player-render-limit:\s*-?\d+', 'player-render-limit: 1', plugin)
        write_file('/plugins/BlueMap/plugin.conf', plugin)
        print("  [OK] plugin.conf optimizado (player-render-limit: 1)")

    # --- 3. Optimizar server.properties ---
    print("3. Optimizando server.properties (distancias y async chunks)...")
    sp = read_file('server.properties')
    if sp:
        sp = re.sub(r'simulation-distance=\d+', 'simulation-distance=5', sp)
        sp = re.sub(r'view-distance=\d+', 'view-distance=7', sp)
        sp = re.sub(r'sync-chunk-writes=(true|false)', 'sync-chunk-writes=false', sp)
        sp = re.sub(r'network-compression-threshold=\d+', 'network-compression-threshold=512', sp)
        write_file('server.properties', sp)
        print("  [OK] server.properties optimizado (sim-distance: 5, view-distance: 7, sync-chunk-writes: false)")

    # --- 4. Optimizar bukkit.yml ---
    print("4. Optimizando bukkit.yml (spawn limits y ticks)...")
    bukkit = read_file('bukkit.yml')
    if bukkit:
        bukkit = re.sub(r'monsters:\s*\d+', 'monsters: 45', bukkit)
        bukkit = re.sub(r'animals:\s*\d+', 'animals: 8', bukkit)
        bukkit = re.sub(r'water-ambient:\s*\d+', 'water-ambient: 2', bukkit)
        bukkit = re.sub(r'ambient:\s*\d+', 'ambient: 1', bukkit)
        bukkit = re.sub(r'monster-spawns:\s*\d+', 'monster-spawns: 4', bukkit)
        bukkit = re.sub(r'water-spawns:\s*\d+', 'water-spawns: 4', bukkit)
        bukkit = re.sub(r'ambient-spawns:\s*\d+', 'ambient-spawns: 4', bukkit)
        write_file('bukkit.yml', bukkit)
        print("  [OK] bukkit.yml optimizado")

    # --- 5. Optimizar spigot.yml ---
    print("5. Optimizando spigot.yml (activation range y hoppers)...")
    spigot = read_file('spigot.yml')
    if spigot:
        spigot = re.sub(r'hopper-check:\s*\d+', 'hopper-check: 8', spigot)
        spigot = re.sub(r'item:\s*2\.5', 'item: 4.0', spigot)
        spigot = re.sub(r'exp:\s*3\.0', 'exp: 6.0', spigot)
        # Activation range
        spigot = re.sub(r'animals:\s*32', 'animals: 16', spigot)
        spigot = re.sub(r'monsters:\s*32', 'monsters: 24', spigot)
        spigot = re.sub(r'misc:\s*16', 'misc: 8', spigot)
        write_file('spigot.yml', spigot)
        print("  [OK] spigot.yml optimizado")

    # --- 6. Recargar configuraciones y verificar CPU ---
    print("6. Verificando uso de CPU actual...")
    time.sleep(3)
    r_res = requests.get(f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/resources", headers=headers, timeout=10)
    if r_res.status_code == 200:
        cpu = r_res.json()['attributes']['resources'].get('cpu_absolute', 0)
        print(f"Uso de CPU actual: {cpu:.2f}%")

    print("\n[EXITO] Todas las optimizaciones aplicadas.")

if __name__ == '__main__':
    optimize_all()
