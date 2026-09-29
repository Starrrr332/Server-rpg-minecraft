import json
import os
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {
    "Authorization": f"Bearer {cfg['api_key']}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 1. Borrar destino previo si existe
print("[1/4] Limpiando plugins/GuildAIEconomy.jar anterior...")
requests.post(f"{base_url}/files/delete", headers=headers, json={"root": "/plugins", "files": ["GuildAIEconomy.jar"]})

# 2. Obtener URL de subida
print("[2/4] Solicitando URL de subida...")
r_up = requests.get(f"{base_url}/files/upload", headers={"Authorization": f"Bearer {cfg['api_key']}"}, params={"directory": "/"})
signed_url = r_up.json().get('attributes', {}).get('url') or r_up.json().get('data', {}).get('attributes', {}).get('url')

# 3. Subir jar local a /
print("[3/4] Subiendo nuevo jar a /...")
local_jar = r"c:\Users\amaro\OneDrive\Desktop\Bot para server\GuildAIEconomy\target\GuildAIEconomy-1.0.0.jar"
with open(local_jar, 'rb') as f:
    requests.post(signed_url, files={'files': ('GuildAIEconomy-1.0.0.jar', f, 'application/java-archive')})

# 4. Renombrar / GuildAIEconomy-1.0.0.jar -> plugins/GuildAIEconomy.jar
print("[4/4] Colocando jar en plugins/GuildAIEconomy.jar...")
payload = {
    "root": "/",
    "files": [
        {
            "from": "GuildAIEconomy-1.0.0.jar",
            "to": "plugins/GuildAIEconomy.jar"
        }
    ]
}
r_mv = requests.put(f"{base_url}/files/rename", headers=headers, json=payload)
print("  Respuesta rename:", r_mv.status_code)
if r_mv.status_code in [200, 204]:
    print("[EXITO] GuildAIEconomy.jar colocado exitosamente en /plugins/")
