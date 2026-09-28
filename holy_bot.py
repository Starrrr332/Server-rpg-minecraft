# holy_bot.py
"""Simple Holy Hosting bot.
Provides two commands via the command line:
  python holy_bot.py status   – get server status
  python holy_bot.py restart  – send a restart command

Configuration is read from `bot_config.json` in the same directory.
"""
import json
import sys
import requests

CONFIG_PATH = "bot_config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def api_request(endpoint, method="GET", payload=None):
    cfg = load_config()
    url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}{endpoint}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    response = requests.request(method, url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

def get_status():
    data = api_request("/resources")
    attrs = data.get("attributes", {})
    resources = attrs.get("resources", {})
    print("=== Server Status ===")
    # Nombre del servidor (puede no estar presente en la respuesta)
    print(f"Name: {attrs.get('name') or 'N/A'}")
    print(f"State: {attrs.get('current_state')}")
    print(f"Uptime: {resources.get('uptime', 'N/A')} seconds")
    # Valores numéricos pueden ser None; usamos 0.0 como fallback para formatear
    cpu = resources.get('cpu_absolute')
    mem = resources.get('memory_bytes')
    disk = resources.get('disk_bytes')
    print(f"CPU: {cpu:.2f}%" if cpu is not None else "CPU: N/A")
    print(f"Memory: {mem/1024/1024:.2f} MB" if mem is not None else "Memory: N/A")
    print(f"Disk: {disk/1024/1024:.2f} MB" if disk is not None else "Disk: N/A")

def restart_server():
    cfg = load_config()
    url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}/power"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    payload = {"signal": "restart"}
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    try:
        response.raise_for_status()
        # The restart endpoint may return no JSON; treat any successful status as success
        print("Restart command sent successfully.")
    except Exception as e:
        print(f"Failed to send restart command: {e}")


def upload_plugins():
    import os, glob, requests, json
    cfg = load_config()
    # Locate compiled plugin JARs
    jar_paths = glob.glob(os.path.join("MinecraftPlugins", "*", "target", "*.jar"))
    if not jar_paths:
        print("No plugin JAR files found to upload.")
        return
    # Base upload request URL (GET signed URL)
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}/files/upload"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    for jar_path in jar_paths:
        jar_name = os.path.basename(jar_path)
        try:
            # Step 1: request signed URL for the target directory
            params = {"directory": "/plugins"}
            resp = requests.get(base_url, headers=headers, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            signed_url = data.get('attributes', {}).get('url')
            if not signed_url:
                raise RuntimeError("Signed URL not found in response")
            # Step 2: upload file to the signed URL
            with open(jar_path, 'rb') as f:
                files = {'files': (jar_name, f, 'application/java-archive')}
                # The upload endpoint expects the same directory field in the form data
                upload_resp = requests.post(signed_url, files=files, data={'directory': '/plugins'}, timeout=60)
                upload_resp.raise_for_status()
            print(f"Uploaded {jar_name} to /plugins successfully.")
        except Exception as e:
            print(f"Failed to upload {jar_name}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python holy_bot.py [status|restart|upload|deploy]")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "status":
        get_status()
    elif cmd == "restart":
        restart_server()
    elif cmd == "upload":
        upload_plugins()
    elif cmd == "deploy":
        upload_plugins()
        restart_server()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
