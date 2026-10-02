# -*- coding: utf-8 -*-
import os
import json
import requests
import time

def main():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}

    print("==================================================")
    print(">> PREPARANDO CHUNKY E INICIANDO PRE-GENERACIÓN")
    print("==================================================")

    # 1. Subir Chunky-Bukkit-1.5.3.jar a /plugins
    local_jar = "Chunky-Bukkit-1.5.3.jar"
    if os.path.exists(local_jar):
        print("[1/4] Subiendo Chunky-Bukkit-1.5.3.jar a /plugins/...")
        try:
            resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": "/plugins"}, timeout=20)
            if resp.status_code == 200:
                signed_url = resp.json().get('attributes', {}).get('url') or resp.json().get('data', {}).get('attributes', {}).get('url')
                if signed_url:
                    with open(local_jar, 'rb') as f:
                        up = requests.post(signed_url, files={'files': (local_jar, f, 'application/octet-stream')}, data={'directory': '/plugins'}, timeout=60)
                        print("  --> Subida a /plugins/ completada:", up.status_code)
        except Exception as e:
            print("  Aviso en subida:", e)

    # 2. Reiniciar servidor para cargar Chunky
    print("\n[2/4] Reiniciando servidor para cargar el plugin Chunky...")
    post_headers = {**headers, "Content-Type": "application/json"}
    try:
        requests.post(f"{base_url}/command", headers=post_headers, json={'command': 'save-all'}, timeout=10)
    except Exception:
        pass

    time.sleep(2)
    requests.post(f"{base_url}/power", headers=post_headers, json={'signal': 'restart'}, timeout=15)
    print("  Señal de reinicio enviada. Monitoreando arranque...")

    for i in range(18):
        time.sleep(5)
        try:
            res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
            if res.status_code == 200:
                st = res.json().get('attributes', {}).get('current_state', 'unknown')
                print(f"  Progreso ({(i+1)*5}s): Estado = {st}")
                if st == 'running':
                    print("  [OK] Servidor ONLINE!")
                    break
        except Exception:
            pass

    time.sleep(4)

    # 3. Iniciar Chunky
    print("\n[3/4] Enviando comandos de Chunky para 50 chunks de radio...")
    commands = [
        "chunky world world",
        "chunky center 0 0",
        "chunky shape circle",
        "chunky radius 50c",
        "chunky start"
    ]

    for cmd in commands:
        print(f"  Ejecutando: {cmd}")
        requests.post(f"{base_url}/command", headers=post_headers, json={'command': cmd}, timeout=10)
        time.sleep(2)

    time.sleep(4)

    # 4. Leer logs
    print("\n[4/4] Leyendo respuesta del plugin Chunky en consola...")
    r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        print("\n--- CONSOLE LOGS ---")
        for l in lines[-20:]:
            print(" ", l.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    main()
