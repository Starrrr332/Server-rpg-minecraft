import os
import json
import requests

CONFIG_PATH = "bot_config.json"
LOCAL_GREMIO_DIR = r"C:\Users\amaro\OneDrive\Desktop\Bot para server\temp_gremio"
REMOTE_BASE_DIR = "/plugins/EliteMobs"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    cfg = load_config()
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}

    print("Subiendo archivos de la actualización del Gremio...")

    # Iterate over all files in temp_gremio
    count = 0
    for root, dirs, files in os.walk(LOCAL_GREMIO_DIR):
        for file in files:
            local_path = os.path.join(root, file)
            rel_path = os.path.relpath(local_path, LOCAL_GREMIO_DIR)
            remote_rel = rel_path.replace("\\", "/")
            remote_dir = f"{REMOTE_BASE_DIR}/{os.path.dirname(remote_rel)}".rstrip("/")

            # Get signed upload URL for this remote directory
            resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": remote_dir}, timeout=30)
            if resp.status_code != 200:
                print(f"Error al obtener URL de subida para {remote_dir}: {resp.status_code} - {resp.text}")
                continue
            
            signed_url = resp.json().get('attributes', {}).get('url')
            if not signed_url:
                signed_url = resp.json().get('data', {}).get('attributes', {}).get('url')

            with open(local_path, 'rb') as f:
                upload_resp = requests.post(signed_url, files={'files': (file, f, 'application/octet-stream')}, data={'directory': remote_dir}, timeout=60)
                if upload_resp.status_code in [200, 204]:
                    count += 1
                    print(f"[{count}] Subido: {remote_rel}")
                else:
                    print(f"Error subiendo {remote_rel}: {upload_resp.status_code} - {upload_resp.text}")

    print(f"\n¡Se subieron {count} archivos exitosamente!")

if __name__ == "__main__":
    main()
