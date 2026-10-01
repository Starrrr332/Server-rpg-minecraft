# -*- coding: utf-8 -*-
import json
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

def check_dir(dir_path):
    r = requests.get(f"{base_url}/files/list", headers=headers, params={"directory": dir_path}, timeout=10)
    if r.status_code == 200:
        items = r.json().get('data', [])
        names = [item['attributes']['name'] for item in items]
        print(f"\n=== Directory: {dir_path} ({len(names)} items) ===")
        for n in names[:25]:
            print("  -", n)
    else:
        print(f"\n=== Directory: {dir_path} === ERROR {r.status_code}: {r.text[:100]}")

def main():
    check_dir("/plugins/EliteMobs")
    check_dir("/plugins/EliteMobs/npcs")
    check_dir("/plugins/EliteMobs/menus")
    check_dir("/plugins/EliteMobs/custombosses")
    check_dir("/plugins/EliteMobs/customitems")

if __name__ == '__main__':
    main()
