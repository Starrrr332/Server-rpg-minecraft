from holy_bot_llm import load_config
import requests

cfg = load_config()
base = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {'Authorization': f"Bearer {cfg['api_key']}", 'User-Agent': 'HolyBot/1.0'}

# Leer webserver.conf
resp = requests.get(f"{base}/files/contents", headers=headers, params={'file': '/plugins/BlueMap/webserver.conf'}, timeout=20)
content = resp.text
print("=== webserver.conf ===")
print(content[:2000])
