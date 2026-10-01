# -*- coding: utf-8 -*-
"""
Script de Despliegue y Corrección de la Tienda del Gremio y NPCs de EliteMobs.
Sincroniza menus, npcs, configs y customquests a la ruta exacta /plugins/EliteMobs/
y configura los comandos abreviados (/tienda, /tiendagremio, /gremio, /shop) en commands.yml.
"""
import os
import json
import requests
import time

CONFIG_PATH = "bot_config.json"
BASE_LAB = r"C:\Users\amaro\OneDrive\Desktop\Bot para server\gremio_aventureros_lab"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def upload_file_to_remote(base_url, headers, local_file_path, remote_dir_path):
    filename = os.path.basename(local_file_path)
    # Get signed upload URL
    resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": remote_dir_path}, timeout=30)
    if resp.status_code != 200:
        print(f"  [!] Error obteniendo URL de subida para {remote_dir_path}: {resp.status_code}")
        return False
    
    signed_url = resp.json().get('attributes', {}).get('url')
    if not signed_url:
        signed_url = resp.json().get('data', {}).get('attributes', {}).get('url')
        
    if not signed_url:
        print(f"  [!] URL firmada inválida para {remote_dir_path}")
        return False

    with open(local_file_path, 'rb') as f:
        upload_resp = requests.post(signed_url, files={'files': (filename, f, 'application/octet-stream')}, data={'directory': remote_dir_path}, timeout=45)
        return upload_resp.status_code in [200, 204]

def main():
    cfg = load_config()
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}

    print("==================================================")
    print(">> INICIANDO CORRECCIÓN Y DESPLIEGUE TIENDA DEL GREMIO")
    print("==================================================")

    # 1. Subir NPCs a /plugins/EliteMobs/npcs
    npcs_dir = os.path.join(BASE_LAB, "npcs")
    remote_npcs = "/plugins/EliteMobs/npcs"
    print(f"\n[1/5] Subiendo NPCs a {remote_npcs}...")
    npc_count = 0
    for f in os.listdir(npcs_dir):
        if f.endswith(".yml"):
            local_p = os.path.join(npcs_dir, f)
            if upload_file_to_remote(base_url, headers, local_p, remote_npcs):
                npc_count += 1
    print(f"  --> {npc_count} NPCs subidos correctamente.")

    # 2. Subir Menús a /plugins/EliteMobs/menus
    menus_dir = os.path.join(BASE_LAB, "menus")
    remote_menus = "/plugins/EliteMobs/menus"
    print(f"\n[2/5] Subiendo Menús a {remote_menus}...")
    menu_count = 0
    for f in os.listdir(menus_dir):
        if f.endswith(".yml"):
            local_p = os.path.join(menus_dir, f)
            if upload_file_to_remote(base_url, headers, local_p, remote_menus):
                menu_count += 1
    print(f"  --> {menu_count} Menús de tienda subidos correctamente.")

    # 3. Subir Configuraciones a /plugins/EliteMobs/
    configs_dir = os.path.join(BASE_LAB, "configs")
    remote_configs = "/plugins/EliteMobs"
    print(f"\n[3/5] Subiendo Configs de Economía a {remote_configs}...")
    cfg_count = 0
    for f in os.listdir(configs_dir):
        if f.endswith(".yml"):
            local_p = os.path.join(configs_dir, f)
            if upload_file_to_remote(base_url, headers, local_p, remote_configs):
                cfg_count += 1
    print(f"  --> {cfg_count} Configs de economía subidas correctamente.")

    # 4. Subir Misiones a /plugins/EliteMobs/customquests
    quests_dir = os.path.join(BASE_LAB, "customquests")
    remote_quests = "/plugins/EliteMobs/customquests"
    print(f"\n[4/5] Subiendo Misiones a {remote_quests}...")
    quest_count = 0
    for f in os.listdir(quests_dir):
        if f.endswith(".yml"):
            local_p = os.path.join(quests_dir, f)
            if upload_file_to_remote(base_url, headers, local_p, remote_quests):
                quest_count += 1
    print(f"  --> {quest_count} Misiones subidas correctamente.")

    # 5. Configurar comandos abreviados (/tienda, /tiendagremio, /gremio, /shop) en commands.yml
    print("\n[5/5] Configurando alias de comandos (/tienda, /tiendagremio, /gremio, /shop) en commands.yml...")
    commands_yml_content = """command-block-overrides: []
ignore-vanilla-permissions: false
aliases:
  tienda:
  - em shop
  tiendagremio:
  - em shop
  gremio:
  - ag
  shop:
  - em shop
  icanhasbukkit:
  - version $1-
"""
    local_cmd_path = "temp_commands.yml"
    with open(local_cmd_path, "w", encoding="utf-8") as f:
        f.write(commands_yml_content)

    if upload_file_to_remote(base_url, headers, local_cmd_path, "/"):
        print("  --> commands.yml actualizado en la raíz del servidor!")
    if os.path.exists(local_cmd_path):
        os.remove(local_cmd_path)

    # 6. Recargar EliteMobs y reiniciar el servidor
    print("\n==================================================")
    print("Recargando EliteMobs y reiniciando servidor...")
    print("==================================================")
    
    post_headers = {**headers, "Content-Type": "application/json"}
    
    try:
        requests.post(f"{base_url}/command", headers=post_headers, json={'command': 'em reload'}, timeout=10)
        print("  Comando 'em reload' enviado.")
        time.sleep(2)
        requests.post(f"{base_url}/command", headers=post_headers, json={'command': 'save-all'}, timeout=10)
        print("  Comando 'save-all' enviado.")
    except Exception as e:
        print("  Aviso comandos:", e)

    time.sleep(2)
    print("Enviando señal de reinicio (RESTART)...")
    r_restart = requests.post(f"{base_url}/power", headers=post_headers, json={'signal': 'restart'}, timeout=15)
    if r_restart.status_code in [200, 204]:
        print("[OK] Señal de reinicio enviada exitosamente.")
    else:
        print(f"[!] Respuesta panel: {r_restart.status_code}")

    print("\nMonitoreando estado del servidor...")
    for i in range(18):
        time.sleep(5)
        try:
            res = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
            if res.status_code == 200:
                st = res.json().get('attributes', {}).get('current_state', 'unknown')
                print(f"  Progreso ({(i+1)*5}s): Estado = {st}")
                if st == 'running':
                    print("\n[ÉXITO FINAL] La tienda del gremio y todos sus menús han sido arreglados y están ONLINE!")
                    break
        except Exception as e:
            print(f"  Esperando... ({e})")

if __name__ == '__main__':
    main()
