import json
import os
import requests
import time

CONFIG_PATH = "bot_config.json"

def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0"
    }

    print("[1/2] Guardando datos del mundo (save-all)...")
    try:
        requests.post(f"{base_url}/command", headers=headers, json={'command': 'save-all'}, timeout=10)
    except Exception as e:
        print("  Info save-all:", e)

    time.sleep(2)

    print("[2/2] Enviando senal de reinicio al servidor...")
    r = requests.post(f"{base_url}/power", headers=headers, json={'signal': 'restart'}, timeout=15)
    
    if r.status_code in [200, 204]:
        print("[OK] Senal de reinicio enviada correctamente.")
    else:
        print(f"Respuesta servidor: {r.status_code} - {r.text[:200]}")

    print("\nMonitoreando estado del servidor...")
    for i in range(16):
        time.sleep(5)
        try:
            res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
            if res.status_code == 200:
                state = res.json().get('attributes', {}).get('current_state', 'unknown')
                print(f"  Estado del servidor ({(i+1)*5}s): {state}")
                if state == 'running':
                    print("\n[EXITO] Servidor ONLINE y cargado exitosamente.")
                    break
        except Exception as e:
            print(f"  Esperando respuesta del panel... ({e})")

if __name__ == "__main__":
    main()
