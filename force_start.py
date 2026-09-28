import requests
import json
import time

def main():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    print("1. Enviando senal 'kill'...")
    requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/power",
        headers=headers,
        json={'signal': 'kill'},
        timeout=10
    )

    time.sleep(4)

    print("2. Enviando senal 'start'...")
    r = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/power",
        headers=headers,
        json={'signal': 'start'},
        timeout=10
    )
    print("Start response:", r.status_code)

if __name__ == '__main__':
    main()
