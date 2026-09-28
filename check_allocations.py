import requests
import json

def check_net():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    # 1. Allocations
    print("=== Puertos / Network Allocations en Pterodactyl ===")
    r = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/network/allocations",
        headers=headers,
        timeout=15
    )
    if r.status_code == 200:
        for a in r.json().get('data', []):
            attrs = a.get('attributes', {})
            print("  IP:", attrs.get('ip'), "Alias:", attrs.get('ip_alias'), "Port:", attrs.get('port'), "Primary:", attrs.get('is_default'))
    else:
        print("  Error:", r.status_code, r.text[:200])

    # 2. Check BlueMap webserver log
    print("\n=== BlueMap webserver log ===")
    r_log = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
        headers=headers,
        params={'file': '/plugins/BlueMap/bluemap/logs/webserver.log'},
        timeout=15
    )
    if r_log.status_code == 200:
        print(r_log.text[-2000:])
    else:
        print("  Status webserver.log:", r_log.status_code)

    # 3. Check server latest.log for bluemap
    print("\n=== Minecraft latest.log (BlueMap search) ===")
    r_mc = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
        headers=headers,
        params={'file': '/logs/latest.log'},
        timeout=20
    )
    if r_mc.status_code == 200:
        lines = r_mc.text.splitlines()
        bm_lines = [l for l in lines if 'bluemap' in l.lower() or 'webserver' in l.lower() or 'bind' in l.lower()]
        for l in bm_lines[-15:]:
            print(" ", l)
    else:
        print("  Status latest.log:", r_mc.status_code)

if __name__ == '__main__':
    check_net()
