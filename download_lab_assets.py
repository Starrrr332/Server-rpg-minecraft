import requests
import json
import os

def download_lab():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    lab = 'gremio_aventureros_lab'

    # 1. Download Root Configs
    root_configs = [
        'AdventurersGuild.yml',
        'Quests.yml',
        'MobCombatSettings.yml',
        'EconomySettings.yml',
        'EliteMobPowers.yml',
        'initialize.yml',
        'config.yml'
    ]

    print("[1/5] Descargando configuraciones base...")
    for fn in root_configs:
        r = requests.get(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
            headers=headers,
            params={'file': f'plugins/EliteMobs/{fn}'},
            timeout=15
        )
        if r.status_code == 200:
            with open(f'{lab}/configs/{fn}', 'wb') as f:
                f.write(r.content)
            print(f"  [OK] {fn} ({len(r.content)} bytes)")
        else:
            print(f"  [!] Error al descargar {fn}: {r.status_code}")

    # 2. Download NPCs
    print("\n[2/5] Descargando NPCs de la Guild...")
    r = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/list",
        headers=headers,
        params={'directory': 'plugins/EliteMobs/npcs'},
        timeout=15
    )
    if r.status_code == 200:
        npc_files = [x['attributes']['name'] for x in r.json().get('data', []) if x['attributes']['name'].endswith('.yml')]
        print(f"  Total NPCs encontrados: {len(npc_files)}")
        for fn in npc_files:
            r_file = requests.get(
                f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
                headers=headers,
                params={'file': f'plugins/EliteMobs/npcs/{fn}'},
                timeout=15
            )
            if r_file.status_code == 200:
                with open(f'{lab}/npcs/{fn}', 'wb') as f:
                    f.write(r_file.content)
        print(f"  [OK] Descargados {len(npc_files)} NPCs.")

    # 3. Download Menus
    print("\n[3/5] Descargando Menus...")
    r = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/list",
        headers=headers,
        params={'directory': 'plugins/EliteMobs/menus'},
        timeout=15
    )
    if r.status_code == 200:
        menu_files = [x['attributes']['name'] for x in r.json().get('data', []) if x['attributes']['name'].endswith('.yml')]
        print(f"  Total Menus encontrados: {len(menu_files)}")
        for fn in menu_files:
            r_file = requests.get(
                f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
                headers=headers,
                params={'file': f'plugins/EliteMobs/menus/{fn}'},
                timeout=15
            )
            if r_file.status_code == 200:
                with open(f'{lab}/menus/{fn}', 'wb') as f:
                    f.write(r_file.content)
        print(f"  [OK] Descargados {len(menu_files)} Menus.")

    # 4. Download Custom Quests
    print("\n[4/5] Descargando Misiones...")
    r = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/list",
        headers=headers,
        params={'directory': 'plugins/EliteMobs/customquests'},
        timeout=15
    )
    if r.status_code == 200:
        quest_files = [x['attributes']['name'] for x in r.json().get('data', []) if x['attributes']['name'].endswith('.yml')]
        print(f"  Total Misiones encontradas: {len(quest_files)}")
        for fn in quest_files:
            r_file = requests.get(
                f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
                headers=headers,
                params={'file': f'plugins/EliteMobs/customquests/{fn}'},
                timeout=15
            )
            if r_file.status_code == 200:
                with open(f'{lab}/customquests/{fn}', 'wb') as f:
                    f.write(r_file.content)
        print(f"  [OK] Descargadas {len(quest_files)} Misiones.")

    # 5. Download Translations
    print("\n[5/5] Descargando Archivos de Traduccion...")
    for fn in ['spanish.csv', 'spanish_data.csv']:
        r = requests.get(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
            headers=headers,
            params={'file': f'plugins/EliteMobs/translations/{fn}'},
            timeout=30
        )
        if r.status_code == 200:
            with open(f'{lab}/translations/{fn}', 'wb') as f:
                f.write(r.content)
            print(f"  [OK] {fn} ({len(r.content)} bytes)")
        else:
            print(f"  [!] Error al descargar {fn}: {r.status_code}")

    print("\n[COMPLETADO] Todos los archivos del Gremio de Aventureros estan en gremio_aventureros_lab/")

if __name__ == '__main__':
    download_lab()
