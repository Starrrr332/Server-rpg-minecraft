import requests
import json

def read_log():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    for p in ['logs/latest.log', '/logs/latest.log', 'latest.log']:
        r = requests.get(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
            headers=headers,
            params={'file': p},
            timeout=15
        )
        print(f"Path '{p}': status {r.status_code}, length {len(r.text) if r.status_code == 200 else 0}")
        if r.status_code == 200:
            lines = r.text.splitlines()
            print("Ultimas 20 lineas:")
            for l in lines[-20:]:
                print(" ", l)
            break

if __name__ == '__main__':
    read_log()
