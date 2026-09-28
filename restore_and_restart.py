import requests
import json
import time

def restore_and_restart():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    print("1. Guardando estado actual con save-all...")
    requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/command",
        headers=headers,
        json={'command': 'save-all'},
        timeout=10
    )
    time.sleep(2)

    print("2. Enviando orden de detencion limpia (stop)...")
    requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/power",
        headers=headers,
        json={'signal': 'stop'},
        timeout=10
    )

    # Wait for offline
    print("3. Esperando que el servidor se apague...")
    is_offline = False
    for i in range(12):
        time.sleep(3)
        try:
            r = requests.get(f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/resources", headers=headers, timeout=5)
            state = r.json()['attributes']['current_state']
            print(f"   Estado: {state} ({i+1}/12)")
            if state == 'offline':
                is_offline = True
                break
        except Exception as e:
            print("   Error consultando estado:", e)

    if not is_offline:
        print("   Servidor tardando en apagar, enviando 'kill' seguro...")
        requests.post(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/power",
            headers=headers,
            json={'signal': 'kill'},
            timeout=10
        )
        time.sleep(4)

    print("4. Restaurando archivos de inventario (.dat) con equipamiento completo...")
    with open('backups_playerdata/f0d03f69-7585-3e09-aaaa-cba59086d8db.dat', 'rb') as f:
        dat_content = f.read()

    r_dat = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/write",
        headers={'Authorization': f"Bearer {cfg['api_key']}"},
        params={'file': 'world/players/data/f0d03f69-7585-3e09-aaaa-cba59086d8db.dat'},
        data=dat_content,
        timeout=15
    )
    print("   Restauracion .dat status:", r_dat.status_code)

    r_dat_old = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/write",
        headers={'Authorization': f"Bearer {cfg['api_key']}"},
        params={'file': 'world/players/data/f0d03f69-7585-3e09-aaaa-cba59086d8db.dat_old'},
        data=dat_content,
        timeout=15
    )
    print("   Restauracion .dat_old status:", r_dat_old.status_code)

    print("5. Iniciando servidor (start)...")
    r_start = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/power",
        headers=headers,
        json={'signal': 'start'},
        timeout=10
    )
    print("   Start signal status:", r_start.status_code)

    # Monitor startup
    print("6. Monitoreando arranque del servidor...")
    for i in range(20):
        time.sleep(4)
        try:
            r = requests.get(f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/resources", headers=headers, timeout=5)
            state = r.json()['attributes']['current_state']
            cpu = r.json()['attributes']['resources']['cpu_absolute']
            print(f"   [{i+1}/20] Estado: {state} | CPU: {cpu}%")
            if state == 'running' and i >= 4:
                # Test bluemap
                try:
                    bm = requests.get('http://38.97.61.71:25898/', timeout=3)
                    if bm.status_code == 200:
                        print("   [OK] Servidor y BlueMap en linea exitosamente!")
                        break
                except:
                    pass
        except Exception as e:
            print("   Esperando respuesta...", e)

    print("¡Proceso completado con exito!")

if __name__ == '__main__':
    restore_and_restart()
