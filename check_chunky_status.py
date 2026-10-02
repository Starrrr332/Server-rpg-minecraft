import json
import requests
import re

def check():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}

    # First send chunky progress command
    requests.post(f"{base_url}/command", headers={**headers, "Content-Type": "application/json"}, json={'command': 'chunky progress'}, timeout=10)

    import time
    time.sleep(1.5)

    r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        chunky_lines = [l for l in lines if 'chunky' in l.lower() or 'task' in l.lower()]
        print("Found", len(chunky_lines), "chunky lines. Displaying last 15:")
        for l in chunky_lines[-15:]:
            print("  ", l.encode('ascii', errors='replace').decode('ascii'))
    else:
        print("Error reading logs:", r_log.status_code)

if __name__ == '__main__':
    check()
