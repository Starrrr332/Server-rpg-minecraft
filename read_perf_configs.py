import requests
import json

def read_configs():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    def get_file(name):
        r = requests.get(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
            headers=headers,
            params={'file': name},
            timeout=10
        )
        return r.text if r.status_code == 200 else ""

    print("=== server.properties (Performance keys) ===")
    sp = get_file('server.properties')
    for l in sp.splitlines():
        if any(k in l.lower() for k in ['view-distance', 'simulation-distance', 'network-compression', 'entity-broadcast-range', 'max-tick-time', 'sync-chunk-writes']):
            print(" ", l)

    print("\n=== spigot.yml (Performance keys) ===")
    spigot = get_file('spigot.yml')
    for l in spigot.splitlines()[:60]:
        print(" ", l)

    print("\n=== bukkit.yml (Performance keys) ===")
    bukkit = get_file('bukkit.yml')
    for l in bukkit.splitlines()[:50]:
        print(" ", l)

if __name__ == '__main__':
    read_configs()
