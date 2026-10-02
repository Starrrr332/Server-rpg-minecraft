# -*- coding: utf-8 -*-
"""
Script para mover Chunky-Bukkit-1.5.3.jar a /plugins/, reiniciar el servidor para que Bukkit lo cargue,
y luego iniciar la pre-generación de 50 chunks (chunky radius 50c).
"""
import os
import json
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
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    print("==================================================")
    print(">> PREPARANDO Y EJECUTANDO CHUNKY EN EL SERVIDOR")
    print("==================================================")

    # Paso 1: Mover/Copiar Chunky-Bukkit-1.5.3.jar a /plugins/
    print("\n[1/4] Copiando Chunky-Bukkit-1.5.3.jar a la carpeta /plugins/...")
    copy_payload = {
        "root": "/",
        "files": [
            {"from": "Chunky-Bukkit-1.5.3.jar", "to": "/plugins/Chunky-Bukkit-1.5.3.jar"}
        ]
    }
    r_copy = requests.post(f"{base_url}/files/copy", headers=headers, json={"location": "Chunky-Bukkit-1.5.3.jar"}, timeout=15)
    
    # También intentamos la API de mover/subir si no estaba
    local_jar_path = "Chunky-Bukkit-1.5.3.jar"
    if os.path.exists(local_jar_path):
        print("  Subiendo Chunky-Bukkit-1.5.3.jar a /plugins/ vía API de subida...")
        resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": "/plugins"}, timeout=30)
        if resp.status_code == 200:
            signed_url = resp.json().get('attributes', {}).get('url') or resp.json().get('data', {}).get('attributes', {}).get('url')
            if signed_url:
                with open(local_jar_path, 'rb') as f:
                    up = requests.post(signed_url, files={'files': ('Chunky-Bukkit-1.5.3.jar', f, 'application/octet-stream')}, data={'directory': '/plugins'}, timeout=60)
                    print("  --> Subida de Chunky a /plugins/ completada:", up.status_code)

    # Paso 2: Reiniciar servidor para cargar Chunky
    print("\n[2/4] Guardando servidor y enviando señal de REINICIO para cargar Chunky...")
    try:
        requests.post(f"{base_url}/command", headers=headers, json={'command': 'save-all'}, timeout=10)
    except Exception as e:
        pass

    time.sleep(2)
    requests.post(f"{base_url}/power", headers=headers, json={'signal': 'restart'}, timeout=15)
    print("  Señal de reinicio enviada. Monitoreando arranque...")

    for i in range(18):
        time.sleep(5)
        try:
            res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
            if res.status_code == 200:
                st = res.json().get('attributes', {}).get('current_state', 'unknown')
                print(f"  Progreso arranque ({(i+1)*5}s): Estado = {st}")
                if st == 'running':
                    print("  [OK] Servidor iniciado y cargado correctamente.")
                    break
        except Exception as e:
            pass

    time.sleep(5)

    # Paso 3: Configurar comandos Chunky (50 chunks radius)
    print("\n[3/4] Enviando comandos de Chunky para pre-generar 50 chunks...")
    cmds = [
        "chunky world world",
        "chunky center 0 0",
        "chunky shape circle",
        "chunky radius 50c",
        "chunky start"
    ]

    for c in cmds:
        print(f"  Ejecutando comando: {c}")
        requests.post(f"{base_url}/command", headers=headers, json={'command': c}, timeout=10)
        time.sleep(2)

    time.sleep(4)

    # Paso 4: Comprobar respuesta en consola
    print("\n[4/4] Verificando logs de la consola del servidor...")
    r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        print("\n--- CONSOLE LOG OUTPUT ---")
        for l in lines[-20:]:
            print(" ", l.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    main()
