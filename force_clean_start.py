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

print("[1/3] Enviando senal kill para asegurar cierre limpio del proceso colgado...")
try:
    requests.post(f"{base_url}/power", headers=headers, json={"signal": "kill"}, timeout=10)
except Exception as e:
    print("  Info kill:", e)

time.sleep(4)

print("[2/3] Enviando senal start para iniciar el servidor...")
resp = requests.post(f"{base_url}/power", headers=headers, json={"signal": "start"}, timeout=15)
print("  Respuesta start:", resp.status_code)

print("[3/3] Monitoreando arranque hasta estado RUNNING...")
for i in range(16):
    time.sleep(5)
    try:
        r = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
        if r.status_code == 200:
            st = r.json().get('attributes', {}).get('current_state', 'unknown')
            print(f"  Estado ({(i+1)*5}s): {st}")
            if st == 'running':
                print("\n[EXITO] ¡Servidor 100% ONLINE y listo para recibir conexiones!")
                break
    except Exception as e:
        print(f"  Esperando... ({e})")
