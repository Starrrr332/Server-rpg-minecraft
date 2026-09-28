import requests
import json

def check_perf():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    # 1. Resources
    r = requests.get(f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/resources", headers=headers, timeout=10)
    if r.status_code == 200:
        res = r.json()['attributes']['resources']
        cpu = res.get('cpu_absolute', 0)
        mem = res.get('memory_bytes', 0) / (1024 * 1024)
        disk = res.get('disk_bytes', 0) / (1024 * 1024)
        uptime = res.get('uptime', 0) / 1000
        print(f"=== USO ACTUAL DEL SERVIDOR ===")
        print(f"CPU: {cpu:.2f}%")
        print(f"Memoria RAM: {mem:.1f} MB")
        print(f"Espacio Disco: {disk:.1f} MB")
        print(f"Uptime: {uptime:.0f} segundos")
    else:
        print("Error recursos:", r.status_code)

    # 2. Check config files in root
    print("\n=== Archivos de configuracion del servidor ===")
    r_files = requests.get(f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/list", headers=headers, timeout=10)
    if r_files.status_code == 200:
        configs = ['server.properties', 'bukkit.yml', 'spigot.yml', 'paper-global.yml', 'purpur.yml']
        existing = []
        for it in r_files.json().get('data', []):
            name = it['attributes']['name']
            if name in configs or 'paper' in name or 'spigot' in name or 'bukkit' in name or 'purpur' in name:
                existing.append(name)
        print("Archivos encontrados:", existing)

    # 3. Check BlueMap render state
    print("\n=== Estado de BlueMap Render ===")
    r_bm = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
        headers=headers,
        params={'file': '/plugins/BlueMap/core.conf'},
        timeout=10
    )
    if r_bm.status_code == 200:
        for line in r_bm.text.splitlines():
            if 'render-thread' in line or 'player-render-limit' in line or 'cooldown' in line:
                print(" ", line)

if __name__ == '__main__':
    check_perf()
