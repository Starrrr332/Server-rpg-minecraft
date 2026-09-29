"""Upload GuildAIEconomy plugin to Pterodactyl server /plugins directory and safely restart the server."""
import json
import os
import requests
import time

CONFIG_PATH = "bot_config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    cfg = load_config()
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0"
    }

    jar_path = r"GuildAIEconomy-1.0.0.jar"
    jar_name = "GuildAIEconomy-1.0.0.jar"
    upload_dir = "/plugins"

    if not os.path.exists(jar_path):
        print(f"[ERROR] No se encuentra el archivo compilado: {jar_path}")
        return

    print(f"[1/4] Solicitando URL de subida para {upload_dir}...")
    resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": upload_dir}, timeout=30)
    resp.raise_for_status()
    
    data = resp.json()
    signed_url = data.get('attributes', {}).get('url') or data.get('data', {}).get('attributes', {}).get('url')
    
    if not signed_url:
        print(f"[ERROR] No se obtuvo URL firmada. Respuesta: {resp.text}")
        return

    print(f"[2/4] Subiendo {jar_name} al servidor Pterodactyl...")
    with open(jar_path, 'rb') as f:
        files = {'files': (jar_name, f, 'application/java-archive')}
        upload_resp = requests.post(signed_url, files=files, timeout=120)
        upload_resp.raise_for_status()
    print("  [OK] ¡Plugin subido con éxito a /plugins!")

    print("[3/4] Guardando mundo del servidor (save-all)...")
    try:
        requests.post(f"{base_url}/command", headers=headers, json={'command': 'save-all'}, timeout=10)
    except Exception as e:
        print("  Advertencia save-all:", e)

    time.sleep(3)

    print("[4/4] Enviando señal de reinicio (restart) al servidor...")
    r = requests.post(f"{base_url}/power", headers=headers, json={'signal': 'restart'}, timeout=15)
    
    if r.status_code in [200, 204]:
        print("  [OK] Señal de reinicio enviada correctamente.")
    else:
        print(f"  Respuesta servidor: {r.status_code} - {r.text[:200]}")

    print("\n⏳ Monitoreando reinicio del servidor...")
    for i in range(12):
        time.sleep(5)
        try:
            res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
            if res.status_code == 200:
                state = res.json().get('attributes', {}).get('current_state', 'unknown')
                print(f"  Estado del servidor ({i*5+5}s): {state}")
                if state == 'running':
                    print("\n✅ ¡Servidor ONLINE y el plugin GuildAIEconomy ha sido instalado y cargado con éxito!")
                    break
        except Exception as e:
            print(f"  Esperando respuesta del panel... ({e})")

if __name__ == "__main__":
    main()
