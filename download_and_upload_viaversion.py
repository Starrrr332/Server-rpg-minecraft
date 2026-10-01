import requests
import json

url = "https://hangar.papermc.io/api/v1/projects/ViaVersion/versions/5.2.1/PAPER/DOWNLOAD"
print("Descargando ViaVersion 5.2.1 desde Hangar...")
r_dl = requests.get("https://api.github.com/repos/ViaVersion/ViaVersion/releases/latest")
if r_dl.status_code == 200:
    assets = r_dl.json().get('assets', [])
    for a in assets:
        if a['name'].endswith('.jar'):
            download_url = a['browser_download_url']
            print("Encontrada versión GitHub:", a['name'], download_url)
            jar_data = requests.get(download_url).content
            with open("ViaVersion.jar", "wb") as f:
                f.write(jar_data)
            print("Descargado ViaVersion.jar localmente (", len(jar_data), "bytes)")
            break

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}", "Content-Type": "application/json"}

print("Solicitando URL de subida...")
r_up = requests.get(f"{base_url}/files/upload", headers={"Authorization": f"Bearer {cfg['api_key']}"}, params={"directory": "/"})
signed_url = r_up.json().get('attributes', {}).get('url') or r_up.json().get('data', {}).get('attributes', {}).get('url')

print("Subiendo ViaVersion.jar a /...")
with open("ViaVersion.jar", "rb") as f:
    requests.post(signed_url, files={'files': ('ViaVersion.jar', f, 'application/java-archive')})

print("Renombrando /ViaVersion.jar -> plugins/ViaVersion.jar...")
payload = {
    "root": "/",
    "files": [{"from": "ViaVersion.jar", "to": "plugins/ViaVersion.jar"}]
}
r_mv = requests.put(f"{base_url}/files/rename", headers=headers, json=payload)
print("Respuesta rename:", r_mv.status_code)
if r_mv.status_code in [200, 204]:
    print("[ÉXITO] ViaVersion.jar subido correctamente a /plugins/")
