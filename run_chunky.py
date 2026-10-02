# -*- coding: utf-8 -*-
"""
Script para iniciar pre-generación de 50 chunks con Chunky si el servidor está vacío.
"""
import json
import requests
import time
import re

def main():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 1. Verificar estado del servidor
    print("[1/3] Verificando estado del servidor...")
    res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
    if res.status_code == 200:
        st = res.json().get('attributes', {}).get('current_state', 'unknown')
        print(f"  Estado del servidor: {st}")
        if st != 'running':
            print("[!] El servidor no está corriendo. Iniciando servidor...")
            requests.post(f"{base_url}/power", headers=headers, json={'signal': 'start'}, timeout=10)
            time.sleep(10)

    # 2. Verificar jugadores conectados
    print("[2/3] Verificando si el servidor está vacío con comando 'list'...")
    requests.post(f"{base_url}/command", headers=headers, json={'command': 'list'}, timeout=10)
    time.sleep(2.5)

    online_count = 0
    try:
        r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
        if r_log.status_code == 200:
            lines = r_log.text.splitlines()
            for l in reversed(lines[-25:]):
                match = re.search(r'There are ([0-9]+) of a max', l, re.IGNORECASE)
                if not match:
                    match = re.search(r'([0-9]+)\s*(?:jugadores|players)\s*(?:conectados|online)', l, re.IGNORECASE)
                if match:
                    online_count = int(match.group(1))
                    print(f"  Línea log detectada: {l.strip()}")
                    break
    except Exception as e:
        print("  Aviso leyendo log:", e)

    if online_count > 0:
        print(f"[CANCELADO] Hay {online_count} jugador(es) conectado(s). No se iniciará Chunky para no generar lag.")
        return

    print("  [OK] Servidor vacío (0 jugadores). Procediendo a configurar Chunky.")

    # 3. Configurar e iniciar Chunky (50 chunks = 50c o 800 bloques)
    print("\n[3/3] Configurando e iniciando Chunky para 50 chunks...")
    commands = [
        "chunky world world",
        "chunky center 0 0",
        "chunky shape circle",
        "chunky radius 50c",
        "chunky start"
    ]

    for cmd in commands:
        print(f"  Enviando comando: {cmd}")
        requests.post(f"{base_url}/command", headers=headers, json={'command': cmd}, timeout=10)
        time.sleep(1.5)

    time.sleep(3)

    # Ver logs resultantes
    print("\n--- RESPUESTA DE CHUNKY EN CONSOLA ---")
    r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        for l in lines[-15:]:
            print(" ", l.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    main()
