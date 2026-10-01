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

def list_dir(p):
    r = requests.get(f"{base_url}/files/list", headers=headers, params={'directory': p}, timeout=10)
    if r.status_code == 200:
        return [item['attributes']['name'] for item in r.json().get('data', [])]
    return []

npc_files = list_dir("/plugins/EliteMobs/npcs")
print(f"Total NPC configs: {len(npc_files)}")

installed_worlds = ["em_adventurers_guild", "skyworld", "skyworld_nether", "world", "world_nether", "world_the_end"]

for name in npc_files:
    if "teleport" in name.lower() or "vigia" in name.lower() or "chaman" in name.lower() or "brasas" in name.lower() or "astrologo" in name.lower() or "maestro" in name.lower():
        content = get_file(f"/plugins/EliteMobs/npcs/{name}")
        if content:
            loc = ""
            for line in content.splitlines():
                if "teleportlocation" in line.lower() or "spawnlocation" in line.lower() or "dungeon" in line.lower():
                    loc += line.strip() + " | "
            print(f"NPC [{name}]: {loc}")
