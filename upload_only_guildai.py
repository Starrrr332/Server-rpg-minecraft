import json
import os
import requests

CONFIG_PATH = "bot_config.json"

def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0"
    }

    jar_path = r"c:\Users\amaro\OneDrive\Desktop\Bot para server\GuildAIEconomy\target\GuildAIEconomy-1.0.0.jar"
    jar_name = "GuildAIEconomy-1.0.0.jar"
    upload_dir = "/plugins"

    if not os.path.exists(jar_path):
        print(f"[ERROR] No se encuentra el archivo compilado: {jar_path}")
        return

    print(f"[1/3] Limpiando version previa en {upload_dir}...")
    try:
        requests.post(
            f"{base_url}/files/delete",
            headers=headers,
            json={"root": upload_dir, "files": [jar_name]},
            timeout=15
        )
    except Exception as e:
        print("  Info:", e)

    print(f"[2/3] Solicitando URL de subida para {upload_dir}...")
    resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": upload_dir}, timeout=30)
    resp.raise_for_status()
    
    data = resp.json()
    signed_url = data.get('attributes', {}).get('url') or data.get('data', {}).get('attributes', {}).get('url')
    
    if not signed_url:
        print(f"[ERROR] No se obtuvo URL firmada. Respuesta: {resp.text}")
        return

    print(f"[3/3] Subiendo {jar_name} ({os.path.getsize(jar_path)} bytes) a Pterodactyl...")
    with open(jar_path, 'rb') as f:
        files = {'files': (jar_name, f, 'application/java-archive')}
        upload_resp = requests.post(signed_url, files=files, timeout=120)
        upload_resp.raise_for_status()
    print("[OK] Plugin GuildAIEconomy v1.2.0 subido con exito a /plugins!")

if __name__ == "__main__":
    main()
