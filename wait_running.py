import json
import requests
import time

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}"}

print("Esperando estado running...")
for i in range(12):
    time.sleep(4)
    r = requests.get(f"{base_url}/resources", headers=headers)
    if r.status_code == 200:
        st = r.json().get('attributes', {}).get('current_state')
        print(f"Estado ({i*4+4}s): {st}")
        if st == 'running':
            print("✅ SERVIDOR ONLINE!")
            break
