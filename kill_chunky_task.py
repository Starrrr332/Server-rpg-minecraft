import json
import requests
import time

def kill_chunky():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json"
    }

    # Pause first
    print("1. Enviando 'chunky pause'...")
    requests.post(f"{base_url}/command", headers=headers, json={"command": "chunky pause"}, timeout=10)
    time.sleep(0.5)

    # Cancel command
    print("2. Enviando 'chunky cancel'...")
    requests.post(f"{base_url}/command", headers=headers, json={"command": "chunky cancel"}, timeout=10)
    time.sleep(0.5)

    # Immediate confirm command
    print("3. Enviando 'chunky confirm'...")
    requests.post(f"{base_url}/command", headers=headers, json={"command": "chunky confirm"}, timeout=10)

    time.sleep(2)

    # Check logs
    r_log = requests.get(f"{base_url}/files/contents", headers={"Authorization": f"Bearer {cfg['api_key']}"}, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        print("\n--- ULTIMAS LINEAS DEL LOG ---")
        for l in lines[-10:]:
            print(" ", l.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    kill_chunky()
