# -*- coding: utf-8 -*-
import json
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}

r = requests.get(f"{base_url}/files/list", headers=headers, params={"directory": "/plugins"}, timeout=10)
if r.status_code == 200:
    items = r.json().get('data', [])
    names = [item['attributes']['name'] for item in items]
    print("Plugins folder contents:", names)
    chunky_plugins = [n for n in names if 'chunky' in n.lower()]
    print("Chunky plugins found:", chunky_plugins)
