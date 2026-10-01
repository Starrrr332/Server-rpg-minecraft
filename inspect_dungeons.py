import requests
import json

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

def list_dir(path):
    r = requests.get(f"{base_url}/files/list", headers=headers, params={'directory': path}, timeout=10)
    if r.status_code == 200:
        return [item['attributes']['name'] for item in r.json().get('data', [])]
    return []

print("--- DIRECTORY / (SERVERS WORLDS) ---")
root_items = list_dir("/")
for item in root_items:
    if "world" in item.lower() or "em_" in item.lower() or "dungeon" in item.lower():
        print(" World/Dungeon Folder:", item)

print("\n--- DIRECTORY /plugins/EliteMobs ---")
em_items = list_dir("/plugins/EliteMobs")
print("EliteMobs contents:", em_items)

print("\n--- DIRECTORY /plugins/EliteMobs/dungeons ---")
dungeons = list_dir("/plugins/EliteMobs/dungeons")
print("EliteMobs dungeons:", dungeons)

print("\n--- DIRECTORY /plugins/EliteMobs/content ---")
content = list_dir("/plugins/EliteMobs/content")
print("EliteMobs content:", content)
