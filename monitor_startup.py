import requests
import json
import time

def monitor():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    print("Monitoreando reinicio del servidor...")
    for i in range(20):
        time.sleep(5)
        try:
            r = requests.get(f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/resources", headers=headers, timeout=10)
            if r.status_code == 200:
                state = r.json().get('attributes', {}).get('current_state')
                print(f"[{i+1}/20] Estado del servidor: {state}")
                if state == 'running':
                    # Check BlueMap port
                    try:
                        res = requests.get("http://38.97.61.71:25898/", timeout=2)
                        print(f"  --> [CONEXION EXITOSA] BlueMap respondio con HTTP {res.status_code}!")
                        return True
                    except Exception as e:
                        print("  --> Puerto 25898 todavia iniciando...")
        except Exception as e:
            print(f"[{i+1}/20] Esperando panel...")

    return False

if __name__ == '__main__':
    monitor()
