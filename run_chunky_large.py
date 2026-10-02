# -*- coding: utf-8 -*-
"""
Script para iniciar y monitorear una pre-generación masiva con Chunky (200 chunks de radio = 3,200 bloques de radio).
Solo se ejecuta si hay 0 jugadores conectados.
"""
import json
import requests
import time
import re

def main():
    config_path = "bot_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 1. Verificar estado del servidor
    print("[1/4] Verificando estado del servidor...")
    res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
    if res.status_code == 200:
        st = res.json().get('attributes', {}).get('current_state', 'unknown')
        print(f"  Estado actual del servidor: {st}")
        if st != 'running':
            print("[!] El servidor no está corriendo. Intentando arrancar...")
            requests.post(f"{base_url}/power", headers=headers, json={'signal': 'start'}, timeout=10)
            time.sleep(15)

    # 2. Verificar jugadores conectados
    print("[2/4] Verificando presencia de jugadores...")
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
                    print(f"  Info de jugadores en log: {l.strip()}")
                    break
    except Exception as e:
        print("  Error leyendo logs:", e)

    if online_count > 0:
        print(f"[CANCELADO] Hay {online_count} jugador(es) en línea. Se cancela la generación para evitar lag.")
        return

    print("  [OK] 0 jugadores en línea. Seguro continuar.")

    # 3. Enviar comandos Chunky (200c = 3,200 bloques de radio ~ 125,660 chunks)
    print("\n[3/4] Enviando comandos Chunky para radio 200c (3,200 bloques de radio)...")
    commands = [
        "chunky quiet 1",       # Evita spam excesivo pero da resúmenes
        "chunky world world",
        "chunky center 0 0",
        "chunky shape circle",
        "chunky radius 200c",
        "chunky start"
    ]

    for cmd in commands:
        print(f"  -> {cmd}")
        requests.post(f"{base_url}/command", headers=headers, json={'command': cmd}, timeout=10)
        time.sleep(1.5)

    # 4. Monitorear progreso de Chunky
    print("\n[4/4] Monitoreando progreso de Chunky en tiempo real...")
    last_printed_line = ""
    start_time = time.time()
    
    # Monitorear durante un máximo de 10 minutos (o hasta completion)
    max_duration = 600 # 10 minutos
    while time.time() - start_time < max_duration:
        time.sleep(8)
        try:
            r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
            if r_log.status_code == 200:
                lines = r_log.text.splitlines()
                # Buscar líneas de Chunky Task
                chunky_lines = [l for l in lines[-30:] if 'Chunky' in l or 'Task' in l or 'Task finished' in l or 'progress' in l.lower()]
                if chunky_lines:
                    latest = chunky_lines[-1].strip()
                    if latest != last_printed_line:
                        last_printed_line = latest
                        clean_line = re.sub(r'\[[0-9:]+\]\s*\[[^\]]+\]:\s*', '', latest)
                        print(f"  [{int(time.time() - start_time)}s] {clean_line}")
                        if "Task finished" in latest or "Task completed" in latest:
                            print("\n[ÉXITO] Pre-generación de Chunky completada satisfactoriamente.")
                            break
        except Exception as e:
            pass

    print("\n--- RESUMEN FINAL DE CONSOLA ---")
    r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
    if r_log.status_code == 200:
        lines = r_log.text.splitlines()
        for l in lines[-12:]:
            clean = re.sub(r'\[[0-9:]+\]\s*\[[^\]]+\]:\s*', '', l)
            print("  ", clean.encode('ascii', errors='replace').decode('ascii'))

if __name__ == '__main__':
    main()
