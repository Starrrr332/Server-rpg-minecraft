import requests, json
cfg = json.load(open('bot_config.json'))
url = f"{cfg['panel_url'].rstrip('/')}/api/client"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"}
resp = requests.get(url, headers=headers, timeout=10)
print(f"Status: {resp.status_code}")
print(f"Headers: {dict(resp.headers)}")
print(f"Body: {resp.text[:500]}")
