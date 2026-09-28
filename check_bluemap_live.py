import requests
import json
import time

def main():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    # 1. Send bluemap reload
    print("Enviando 'bluemap reload' a la consola...")
    r = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/command",
        headers=headers,
        json={'command': 'bluemap reload'},
        timeout=15
    )
    print("Status comando:", r.status_code)

    time.sleep(3)

    # 2. Check if webserver responds on ports
    for port in [25898, 19618, 8100]:
        for host in ['ut09.holy.gg', '38.97.61.71']:
            try:
                res = requests.get(f"http://{host}:{port}/", timeout=2)
                print(f"[CONECTADO] http://{host}:{port}/ -> Status: {res.status_code}")
            except Exception as e:
                pass

if __name__ == '__main__':
    main()
