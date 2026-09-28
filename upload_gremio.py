"""Upload gremio ZIP and decompress it on the server via Pterodactyl API."""
import json
import requests

CONFIG_PATH = "bot_config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    cfg = load_config()
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    zip_path = r"C:\Users\amaro\OneDrive\Desktop\Bot para server\actualizacion_gremio_aventureros.zip"
    zip_name = "actualizacion_gremio_aventureros.zip"
    target_dir = "/plugins/EliteMobs"
    upload_dir = "/plugins"  # This directory worked before

    # Step 1: Get signed upload URL for root
    print(f"[1/3] Getting signed upload URL...")
    resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": upload_dir}, timeout=30)
    resp.raise_for_status()
    data = resp.json().get('data', {})
    signed_url = data.get('url') or data.get('attributes', {}).get('url')
    if not signed_url:
        print("ERROR: Could not get signed URL")
        return

    # Step 2: Upload the ZIP file
    print(f"[2/3] Uploading {zip_name} to {target_dir}...")
    with open(zip_path, 'rb') as f:
        files = {'files': (zip_name, f, 'application/zip')}
        upload_resp = requests.post(signed_url, files=files, data={'directory': upload_dir}, timeout=120)
        upload_resp.raise_for_status()
    print(f"  ZIP uploaded successfully!")

    # Step 3: Decompress the ZIP on the server
    print(f"[3/3] Decompressing {zip_name} into {target_dir}...")
    # Try decompressing from target_dir first (EliteMobs)
    decompress_resp = requests.post(
        f"{base_url}/files/decompress",
        headers={**headers, "Content-Type": "application/json", "Accept": "application/json"},
        json={"root": target_dir, "file": f"../{zip_name}"},
        timeout=120,
    )
    if decompress_resp.status_code != 204:
        # Fallback: decompress from /plugins
        print("  Trying decompress from /plugins...")
        decompress_resp = requests.post(
            f"{base_url}/files/decompress",
            headers={**headers, "Content-Type": "application/json", "Accept": "application/json"},
            json={"root": "/plugins", "file": zip_name},
            timeout=120,
        )
        decompress_resp.raise_for_status()
    print("  Decompressed successfully!")

    # Step 4: Delete the ZIP file from the server (cleanup)
    print("Cleaning up ZIP file from server...")
    delete_resp = requests.post(
        f"{base_url}/files/delete",
        headers={**headers, "Content-Type": "application/json", "Accept": "application/json"},
        json={"root": "/plugins", "files": [zip_name]},
        timeout=30,
    )
    delete_resp.raise_for_status()
    print("  Cleanup done!")

    print("\nAll done! Gremio update applied.")

if __name__ == "__main__":
    main()
