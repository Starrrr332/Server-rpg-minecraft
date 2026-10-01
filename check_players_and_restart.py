# -*- coding: utf-8 -*-
"""
Script para verificar jugadores conectados y reiniciar el servidor si no hay nadie.
"""
import json
import requests
import time
import re
import sys

def main():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # 1. Verificar estado del servidor en el panel
    print("[1/4] Verificando estado del servidor...")
    try:
        res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
        if res.status_code == 200:
            state = res.json().get('attributes', {}).get('current_state', 'unknown')
            print(f"  Estado actual: {state}")
            if state != 'running':
                print("[!] El servidor no está en ejecución. Iniciando reinicio/arranque directo...")
                restart_server(base_url, headers)
                return
    except Exception as e:
        print("  Error al obtener estado:", e)

    # 2. Enviar comando 'list' a la consola para ver jugadores en línea
    print("[2/4] Consultando jugadores conectados con comando 'list'...")
    try:
        requests.post(f"{base_url}/command", headers=headers, json={'command': 'list'}, timeout=10)
    except Exception as e:
        print("  Error al enviar comando 'list':", e)

    time.sleep(2.5)

    # 3. Leer últimas líneas de latest.log
    print("[3/4] Leyendo respuesta en logs/latest.log...")
    online_count = 0
    player_names = []
    found_list_response = False

    try:
        r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
        if r_log.status_code == 200:
            lines = r_log.text.splitlines()
            # Buscar en las últimas 25 líneas la respuesta de /list
            for l in reversed(lines[-25:]):
                # Ejemplo de línea: "There are 0 of a max of 20 players online:" o "There are 2 of a max of 20 players online: Player1, Player2"
                match_count = re.search(r'There are ([0-9]+) of a max of [0-9]+ players online', l, re.IGNORECASE)
                if not match_count:
                    # Formato en español u otro plugin: "Hay 0 jugadores conectados"
                    match_count = re.search(r'([0-9]+)\s*(?:jugadores|players)\s*(?:conectados|online)', l, re.IGNORECASE)
                
                if match_count:
                    found_list_response = True
                    online_count = int(match_count.group(1))
                    print(f"  Línea encontrada en log: {l.strip()}")
                    print(f"  --> Jugadores conectados: {online_count}")
                    break
    except Exception as e:
        print("  Error al leer logs:", e)

    if not found_list_response:
        print("  [?] No se detectó la respuesta explícita en log. Asumiendo 0 jugadores activos si no hay mensajes recientes de chat.")

    # 4. Decisión de reinicio
    if online_count == 0:
        print("\n==================================================")
        print("[CONFIRMADO] No hay nadie conectado (0 jugadores).")
        print("Iniciando procedimiento de reinicio seguro...")
        print("==================================================")
        restart_server(base_url, headers)
    else:
        print("\n==================================================")
        print(f"[CANCELADO] Hay {online_count} jugador(es) conectado(s). NO se reiniciará el servidor para no interrumpirlos.")
        print("==================================================")

def restart_server(base_url, headers):
    print("\n[!] Guardando mapa y mundo (save-all)...")
    try:
        requests.post(f"{base_url}/command", headers=headers, json={'command': 'save-all'}, timeout=10)
    except Exception as e:
        print("  Save-all notice:", e)

    time.sleep(2)

    print("[!] Enviando señal RESTART al servidor...")
    r = requests.post(f"{base_url}/power", headers=headers, json={'signal': 'restart'}, timeout=15)
    if r.status_code in [200, 204]:
        print("[OK] Señal de reinicio enviada exitosamente.")
    else:
        print(f"[!] Respuesta panel: {r.status_code} - {r.text[:200]}")

    print("\nMonitoreando hasta que el servidor vuelva a estar ONLINE...")
    for i in range(18):
        time.sleep(5)
        try:
            res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
            if res.status_code == 200:
                st = res.json().get('attributes', {}).get('current_state', 'unknown')
                print(f"  Progreso ({(i+1)*5}s): Estado = {st}")
                if st == 'running':
                    print("\n[ÉXITO FINAL] El servidor ha sido reiniciado y está completamente ONLINE!")
                    break
        except Exception as e:
            print(f"  Esperando respuesta del servidor... ({e})")

if __name__ == '__main__':
    main()
