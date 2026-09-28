import requests
import json
import re

def optimize():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    # 1. Update core.conf
    print("Optimizando core.conf para tiempo real...")
    r_core = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
        headers=headers,
        params={'file': '/plugins/BlueMap/core.conf'},
        timeout=15
    )
    if r_core.status_code == 200:
        c_text = r_core.text
        # Change update-cooldown to 3 seconds (real-time tile updates)
        c_text = re.sub(r'update-cooldown:\s*\d+', 'update-cooldown: 3', c_text)
        # Change full-update-interval to 5 minutes
        c_text = re.sub(r'full-update-interval:\s*\d+', 'full-update-interval: 5', c_text)
        # Give 2 render threads for fast live rendering
        c_text = re.sub(r'render-thread-count:\s*\d+', 'render-thread-count: 2', c_text)

        r_w = requests.post(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/write?file=/plugins/BlueMap/core.conf",
            headers={**headers, 'Content-Type': 'application/octet-stream'},
            data=c_text.encode('utf-8'),
            timeout=15
        )
        print("  core.conf status:", r_w.status_code)

    # 2. Update webserver.conf
    print("Optimizando webserver.conf (SSE y Cache-Control sin retraso)...")
    r_web = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
        headers=headers,
        params={'file': '/plugins/BlueMap/webserver.conf'},
        timeout=15
    )
    if r_web.status_code == 200:
        w_text = r_web.text
        # Remove tile 24h cache so live blocks update immediately in browser
        w_text = w_text.replace('"Cache-Control": "public, max-age=86400, stale-if-error=604800"', '"Cache-Control": "no-cache, must-revalidate"')
        w_text = w_text.replace('"CDN-Cache-Control": "max-age=60"', '"CDN-Cache-Control": "no-cache"')

        r_w2 = requests.post(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/write?file=/plugins/BlueMap/webserver.conf",
            headers={**headers, 'Content-Type': 'application/octet-stream'},
            data=w_text.encode('utf-8'),
            timeout=15
        )
        print("  webserver.conf status:", r_w2.status_code)

    # 3. Reload bluemap configs
    print("Recargando BlueMap...")
    r_cmd = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/command",
        headers=headers,
        json={'command': 'bluemap reload'},
        timeout=10
    )
    print("  bluemap reload status:", r_cmd.status_code)

if __name__ == '__main__':
    optimize()
