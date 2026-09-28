import requests, json
cfg = json.load(open('bot_config.json'))
url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}/websocket"
headers = {"Authorization": f"Bearer {cfg['api_key']}"}
resp = requests.get(url, headers=headers, timeout=10)
print("Status:", resp.status_code)
print("Body:", resp.text[:2000])
