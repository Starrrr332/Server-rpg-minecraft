import requests
import json
import time

def restart():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    # 1. Save all
    print("Guardando mundo del servidor (save-all)...")
    try:
        requests.post(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/command",
            headers=headers,
            json={'command': 'save-all'},
            timeout=10
        )
    except Exception as e:
        print("Save-all error (continuando):", e)

    time.sleep(3)

    # 2. Restart signal
    print("Enviando senal de reinicio (restart)...")
    r = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/power",
        headers=headers,
        json={'signal': 'restart'},
        timeout=15
    )
    print("Status reinicio:", r.status_code)
    if r.status_code in [200, 204]:
        print("[OK] Servidor reiniciandose. Esperando a que suba...")
    else:
        print("Respuesta:", r.text[:200])

if __name__ == '__main__':
    restart()
