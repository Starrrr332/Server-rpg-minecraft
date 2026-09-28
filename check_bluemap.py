from holy_bot_llm import load_config, api_request
import requests

# Estado del servidor
data = api_request('/resources')
attrs = data.get('attributes', {})
print('Estado:', attrs.get('current_state'))
uptime = (attrs.get('resources', {}).get('uptime') or 0) / 1000
print('Uptime:', round(uptime), 'segundos')

# Log fresco del servidor
cfg = load_config()
url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}/files/contents"
headers = {'Authorization': f"Bearer {cfg['api_key']}", 'User-Agent': 'HolyBot/1.0'}
resp = requests.get(url, headers=headers, params={'file': '/logs/latest.log'}, timeout=20)
text = resp.text
lines = text.strip().split('\n')
print('Lineas en log:', len(lines))
print('Ultima linea:', lines[-1][:60] if lines else 'N/A')

# Buscar BlueMap
found = [l.strip() for l in lines if any(x in l for x in ['BlueMap', 'bluemap', '8100'])]
if found:
    print('\n--- BlueMap encontrado ---')
    for l in found:
        print(l)
else:
    print('\nBlueMap NO encontrado. Ultimas 15 lineas:')
    for l in lines[-15:]:
        print(l.strip())
