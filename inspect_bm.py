import requests
import json
import time

def inspect_bluemap():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    # 1. Read core.conf
    r = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
        headers=headers,
        params={'file': '/plugins/BlueMap/core.conf'},
        timeout=15
    )
    print("core.conf status:", r.status_code)
    if r.status_code == 200:
        for line in r.text.splitlines()[:20]:
            print(" ", line)

    # 2. Check plugins on server via console command
    print("\n--- Enviando comando 'bluemap' a la consola ---")
    r_cmd = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/command",
        headers=headers,
        json={"command": "bluemap"},
        timeout=15
    )
    print("Command status:", r_cmd.status_code)

    # Wait 2 seconds and check console output or logs
    time.sleep(2)
    # Read latest.log
    r_log = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
        headers=headers,
        params={'file': 'logs/latest.log'},
        timeout=15
    )
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        print("\nUltimas 15 lineas de latest.log:")
        for l in lines[-15:]:
            print(" ", l)

if __name__ == '__main__':
    inspect_bluemap()
