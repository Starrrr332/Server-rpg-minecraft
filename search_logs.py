# -*- coding: utf-8 -*-
import json
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

def main():
    r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=15)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        print(f"Total log lines: {len(lines)}")
        print("\n--- SEARCHING FOR COMMANDS & ERRORS IN LOGS ---")
        keywords = ['shop', 'tienda', 'gremio', 'em', 'npc', 'unknown command', 'issued server command']
        matching = []
        for l in lines:
            l_lower = l.lower()
            if any(k in l_lower for k in keywords):
                matching.append(l)
        
        print(f"Found {len(matching)} matching lines:")
        for m in matching[-35:]:
            print(" ", m.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    main()
