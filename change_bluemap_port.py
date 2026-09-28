from holy_bot_llm import load_config
import requests

cfg = load_config()
base = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {'Authorization': f"Bearer {cfg['api_key']}", 'User-Agent': 'HolyBot/1.0'}

# Leer webserver.conf
resp = requests.get(f"{base}/files/contents", headers=headers, params={'file': '/plugins/BlueMap/webserver.conf'}, timeout=20)
content = resp.text

# Cambiar puerto 8100 → 25898
new_content = content.replace('port: 8100', 'port: 25898')
print("Cambio realizado:", 'port: 25898' in new_content)

# Escribir de vuelta
r = requests.post(
    f"{base}/files/write?file=/plugins/BlueMap/webserver.conf",
    headers={**headers, 'Content-Type': 'application/octet-stream'},
    data=new_content.encode('utf-8'),
    timeout=20
)
print('Status:', r.status_code)
if r.status_code in (200, 204):
    print('webserver.conf actualizado a puerto 25898!')
else:
    print('Error:', r.text[:200])
