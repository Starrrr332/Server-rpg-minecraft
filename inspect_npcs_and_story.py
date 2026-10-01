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

print("=== /plugins/EliteMobs/customquests/story_dungeons ===")
print(list_dir("/plugins/EliteMobs/customquests/story_dungeons"))

print("\n=== /plugins/EliteMobs/npcs ===")
npcs = list_dir("/plugins/EliteMobs/npcs")
print(npcs)
