# -*- coding: utf-8 -*-
import os
import json
import requests

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {"Authorization": f"Bearer {cfg['api_key']}"}

def main():
    local_jar = r"C:\Users\amaro\OneDrive\Desktop\Bot para server\Chunky-Bukkit-1.5.3.jar"
    if not os.path.exists(local_jar):
        print("ERROR: No se encuentra localmente Chunky-Bukkit-1.5.3.jar")
        return

    print("[1] Solicitando URL de subida para /plugins ...")
    resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": "/plugins"}, timeout=30)
    print("  Respuesta upload endpoint:", resp.status_code)
    upload_url = resp.json().get('attributes', {}).get('url')
    if not upload_url:
        upload_url = resp.json().get('data', {}).get('attributes', {}).get('url')
    
    print("  Upload URL:", upload_url)

    print("[2] Subiendo Chunky-Bukkit-1.5.3.jar a /plugins ...")
    with open(local_jar, 'rb') as f:
        files = {'files': ('Chunky-Bukkit-1.5.3.jar', f, 'application/java-archive')}
        # Pterodactyl expects directory query parameter in the signed URL or form data
        u_resp = requests.post(f"{upload_url}&directory=%2Fplugins", files=files, timeout=120)
        print("  Respuesta subida:", u_resp.status_code, u_resp.text[:150])

    print("[3] Verificando presencia de Chunky en /plugins ...")
    r_list = requests.get(f"{base_url}/files/list", headers=headers, params={"directory": "/plugins"}, timeout=10)
    if r_list.status_code == 200:
        names = [item['attributes']['name'] for item in r_list.json().get('data', [])]
        chunky_found = [n for n in names if 'chunky' in n.lower()]
        print("  Archivos Chunky en /plugins:", chunky_found)

if __name__ == '__main__':
    main()
