# -*- coding: utf-8 -*-
"""
Script final para reiniciar el servidor, verificar la carga de Chunky en /plugins,
y lanzar la pre-generación de 50 chunks (50c / 800 bloques).
"""
import json
import requests
import time

def main():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    post_headers = {**headers, "Content-Type": "application/json"}

    print("==================================================")
    print(">> REINICIANDO SERVIDOR Y LANZANDO CHUNKY (50 CHUNKS)")
    print("==================================================")

    # 1. Enviar save-all y restart
    try:
        requests.post(f"{base_url}/command", headers=post_headers, json={'command': 'save-all'}, timeout=10)
    except Exception:
        pass

    time.sleep(2)
    requests.post(f"{base_url}/power", headers=post_headers, json={'signal': 'restart'}, timeout=15)
    print("[1/3] Señal de reinicio enviada. Esperando a que el servidor vuelva a estar ONLINE...")

    for i in range(20):
        time.sleep(5)
        try:
            res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
            if res.status_code == 200:
                st = res.json().get('attributes', {}).get('current_state', 'unknown')
                print(f"  Progreso arranque ({(i+1)*5}s): Estado = {st}")
                if st == 'running':
                    print("  [OK] Servidor iniciado y cargado!")
                    break
        except Exception:
            pass

    time.sleep(5)

    # 2. Configurar e Iniciar Chunky
    print("\n[2/3] Configurando e iniciando pre-generación Chunky (50c)...")
    commands = [
        "chunky world world",
        "chunky center 0 0",
        "chunky shape circle",
        "chunky radius 50c",
        "chunky start"
    ]

    for cmd in commands:
        print(f"  Ejecutando consola: {cmd}")
        requests.post(f"{base_url}/command", headers=post_headers, json={'command': cmd}, timeout=10)
        time.sleep(2)

    time.sleep(5)

    # 3. Leer logs finales de consola
    print("\n[3/3] Leyendo logs de consola para confirmar Chunky...")
    r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        print("\n--- ÚLTIMAS LÍNEAS DE CONSOLA ---")
        for l in lines[-25:]:
            print(" ", l.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    main()
