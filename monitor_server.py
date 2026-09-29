import json
import requests
import time

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}"}

print("Monitoreando reinicio del servidor...")
for i in range(16):
    time.sleep(5)
    try:
        r = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
        if r.status_code == 200:
            st = r.json().get('attributes', {}).get('current_state', 'unknown')
            print(f"  Estado ({(i+1)*5}s): {st}")
            if st == 'running':
                print("[OK] Servidor ONLINE!")
                break
    except Exception as e:
        print(f"  Esperando... ({e})")
