# -*- coding: utf-8 -*-
import json
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

def main():
    r = requests.get(f"{base_url}/files/list", headers=headers, params={"directory": "/"}, timeout=10)
    if r.status_code == 200:
        items = r.json().get('data', [])
        names = [item['attributes']['name'] for item in items]
        print("Root server files:", names)
        if 'commands.yml' in names:
            r_cmd = requests.get(f"{base_url}/files/contents", headers=headers, params={"file": "commands.yml"}, timeout=10)
            print("\n--- commands.yml content ---")
            print(r_cmd.text)

if __name__ == '__main__':
    main()
