import json
import requests

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {
    "Authorization": f"Bearer {cfg['api_key']}",
    "Content-Type": "application/json"
}

r = requests.post(f"{base_url}/command", headers=headers, json={"command": "guildai prices"})
print("Respuesta comando:", r.status_code)
