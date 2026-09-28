from holy_bot_llm import load_config
import requests

cfg = load_config()
url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}/files/contents"
headers = {'Authorization': f"Bearer {cfg['api_key']}", 'User-Agent': 'HolyBot/1.0'}

# Leer el core.conf actual
resp = requests.get(url, headers=headers, params={'file': '/plugins/BlueMap/core.conf'}, timeout=20)
content = resp.text
print("=== core.conf actual ===")
print(content[:2000])
