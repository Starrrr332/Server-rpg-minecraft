import requests
import json

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

def list_dir(p):
    r = requests.get(f"{base_url}/files/list", headers=headers, params={'directory': p}, timeout=10)
    if r.status_code == 200:
        return [item['attributes']['name'] for item in r.json().get('data', [])]
    return []

def get_file(p):
    r = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': p}, timeout=10)
    if r.status_code == 200:
        return r.text
    return None

files = list_dir("/plugins/Chunky")
print("Archivos en /plugins/Chunky:", files)

for f in files:
    content = get_file(f"/plugins/Chunky/{f}")
    if content:
        print(f"\n=== /plugins/Chunky/{f} ===")
        for line in content.splitlines()[:30]:
            print(line)
