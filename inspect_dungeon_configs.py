import requests
import json

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

def get_file(path):
    r = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': path}, timeout=10)
    if r.status_code == 200:
        return r.text
    return None

print("=== /plugins/EliteMobs/dungeons.yml ===")
dung_yml = get_file("/plugins/EliteMobs/dungeons.yml")
if dung_yml:
    for line in dung_yml.splitlines()[:40]:
        print(line)

print("\n=== /plugins/EliteMobs/npcs/story_dungeons_quest_giver.yml ===")
sqg = get_file("/plugins/EliteMobs/npcs/story_dungeons_quest_giver.yml")
if sqg:
    for line in sqg.splitlines()[:30]:
        print(line)
