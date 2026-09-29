import json
import os
import requests
import time

CONFIG_PATH = "bot_config.json"

def main():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0"
    }

    local_jar_path = r"c:\Users\amaro\OneDrive\Desktop\Bot para server\GuildAIEconomy\target\GuildAIEconomy-1.0.0.jar"
    jar_name = "GuildAIEconomy-1.0.0.jar"
    plugins_dir = "/plugins"

    if not os.path.exists(local_jar_path):
        print(f"[ERROR] Archivo compilado local no existe: {local_jar_path}")
        return

    # 1. Limpieza de archivos desubicados en / y en /plugins
    print("[1/5] Limpiando jar previo en la raiz / y en /plugins...")
    try:
        requests.post(f"{base_url}/files/delete", headers=headers, json={"root": "/", "files": [jar_name]}, timeout=15)
    except Exception as e:
        print("  Info:", e)

    try:
        requests.post(f"{base_url}/files/delete", headers=headers, json={"root": plugins_dir, "files": [jar_name]}, timeout=15)
    except Exception as e:
        print("  Info:", e)

    # 2. Obtener URL de subida firmada para /plugins
    print(f"[2/5] Solicitando URL firmada para {plugins_dir}...")
    resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": plugins_dir}, timeout=30)
    resp.raise_for_status()
    
    data = resp.json()
    signed_url = data.get('attributes', {}).get('url') or data.get('data', {}).get('attributes', {}).get('url')
    
    if not signed_url:
        print(f"[ERROR] No se obtuvo URL firmada: {resp.text}")
        return

    # 3. Subir archivo a /plugins (pasando data={'directory': plugins_dir})
    print(f"[3/5] Subiendo {jar_name} directamente a /plugins...")
    with open(local_jar_path, 'rb') as f:
        files = {'files': (jar_name, f, 'application/java-archive')}
        upload_resp = requests.post(signed_url, files=files, data={'directory': plugins_dir}, timeout=120)
        upload_resp.raise_for_status()

    # 4. Verificar subida en /plugins
    print("[4/5] Verificando presencia de jar en /plugins...")
    v_resp = requests.get(f"{base_url}/files/list", headers=headers, params={"directory": plugins_dir}, timeout=15)
    found = False
    if v_resp.status_code == 200:
        for item in v_resp.json().get('data', []):
            attr = item.get('attributes', {})
            if attr.get('name') == jar_name:
                found = True
                print(f"  [CONFIRMADO] Archivo encontrado: /plugins/{jar_name} ({attr.get('size')} bytes)")
                break

    if not found:
        print(f"[WARN] No se vio el archivo en la lista de /plugins. Intentando mover desde la raiz si cayo en /...")
        requests.post(f"{base_url}/files/move", headers=headers, json={"root": "/", "files": [jar_name], "to": f"/plugins/{jar_name}"}, timeout=15)

    # 5. Reiniciar servidor y monitorear
    print("\n[5/5] Enviando orden de reinicio al servidor Pterodactyl...")
    try:
        requests.post(f"{base_url}/command", headers=headers, json={'command': 'save-all'}, timeout=10)
    except Exception:
        pass

    time.sleep(2)
    requests.post(f"{base_url}/power", headers=headers, json={'signal': 'restart'}, timeout=15)

    print("Monitoreando arranque del servidor...")
    for i in range(16):
        time.sleep(5)
        try:
            r = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
            if r.status_code == 200:
                st = r.json().get('attributes', {}).get('current_state', 'unknown')
                print(f"  Estado ({i*5+5}s): {st}")
                if st == 'running':
                    print("\n[EXITO] ¡Servidor ONLINE y reiniciado correctamente!")
                    break
        except Exception as e:
            print(f"  Esperando respuesta ({e})...")

if __name__ == "__main__":
    main()
