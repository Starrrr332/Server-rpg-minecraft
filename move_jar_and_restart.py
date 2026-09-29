import json
import requests
import time

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {
    "Authorization": f"Bearer {cfg['api_key']}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 1. Renombrar / Mover desde la raiz / a /plugins/GuildAIEconomy.jar
print("[1/3] Moviendo GuildAIEconomy-1.0.0.jar de / a plugins/GuildAIEconomy.jar...")
payload = {
    "root": "/",
    "files": [
        {
            "from": "GuildAIEconomy-1.0.0.jar",
            "to": "plugins/GuildAIEconomy.jar"
        }
    ]
}

r = requests.put(f"{base_url}/files/rename", headers=headers, json=payload)
print("  Respuesta rename:", r.status_code, r.text)

# 2. Verificar que plugins/GuildAIEconomy.jar ahora sí existe
print("[2/3] Verificando presencia en /plugins...")
r_list = requests.get(f"{base_url}/files/list", headers=headers, params={"directory": "/plugins"})
found = False
if r_list.status_code == 200:
    for item in r_list.json().get("data", []):
        attr = item.get("attributes", {})
        if "GuildAIEconomy" in attr.get("name"):
            print(f"  [OK ENCONTRADO] {attr.get('name')} ({attr.get('size')} bytes)")
            found = True

if not found:
    print("[ERROR] No se pudo mover el archivo. Intentando subirlo comprimido en zip...")

# 3. Reiniciar servidor
print("[3/3] Reiniciando el servidor...")
requests.post(f"{base_url}/power", headers=headers, json={"signal": "restart"})
print("✅ Reinicio enviado!")
