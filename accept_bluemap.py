from holy_bot_llm import load_config
import requests

cfg = load_config()
base = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {'Authorization': f"Bearer {cfg['api_key']}", 'User-Agent': 'HolyBot/1.0'}

# Leer el core.conf actual
resp = requests.get(f"{base}/files/contents", headers=headers, params={'file': '/plugins/BlueMap/core.conf'}, timeout=20)
content = resp.text

# Cambiar accept-download: false por true
new_content = content.replace('accept-download: false', 'accept-download: true')
print("Cambio realizado:", 'accept-download: true' in new_content)

# Escribir el archivo de vuelta
write_url = f"{base}/files/write?file=/plugins/BlueMap/core.conf"
r = requests.post(write_url, headers={**headers, 'Content-Type': 'application/octet-stream'}, data=new_content.encode('utf-8'), timeout=20)
print('Status escritura:', r.status_code)
if r.status_code in (200, 204):
    print('core.conf actualizado correctamente!')
else:
    print('Error:', r.text[:200])
