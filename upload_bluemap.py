from holy_bot_llm import load_config
import requests

cfg = load_config()
headers = {
    'Authorization': f"Bearer {cfg['api_key']}",
    'User-Agent': 'Mozilla/5.0 HolyBot/1.0',
}

url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}/files/upload"

# Obtener URL de subida
resp = requests.get(url, headers=headers, timeout=15)
resp.raise_for_status()
upload_url = resp.json()['attributes']['url']
print('URL de subida obtenida')

# Subir el archivo
with open('BlueMap-spigot.jar', 'rb') as f:
    r = requests.post(
        upload_url,
        files={'files': ('BlueMap-spigot.jar', f, 'application/java-archive')},
        params={'directory': '/plugins'},
        timeout=120
    )
    print('Status:', r.status_code)
    if r.status_code in (200, 204):
        print('BlueMap-spigot.jar subido correctamente!')
    else:
        print('Respuesta:', r.text[:300])
