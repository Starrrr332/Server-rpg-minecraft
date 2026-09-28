from holy_bot_llm import load_config
import requests

cfg = load_config()
headers = {
    'Authorization': f"Bearer {cfg['api_key']}",
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 HolyBot/1.0',
}

url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}/files/contents"
resp = requests.get(url, headers=headers, params={'file': '/logs/latest.log'}, timeout=20)
text = resp.text

found = False
for line in text.split('\n'):
    if any(x in line for x in ['BlueMap', 'bluemap', '8100', 'blue']):
        print(line.strip())
        found = True

if not found:
    print("No se encontraron lineas de BlueMap en el log.")
    print("\n--- Ultimas 30 lineas ---")
    for l in text.strip().split('\n')[-30:]:
        print(l)
