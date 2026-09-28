import os
import json
import time
import requests

def main():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    def fetch_file(path):
        for attempt in range(5):
            try:
                r = requests.get(
                    f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
                    headers=headers,
                    params={'file': path},
                    timeout=15
                )
                if r.status_code == 200:
                    return r.text
                elif r.status_code == 404:
                    return None
            except Exception as e:
                pass
            time.sleep(2)
        return None

    cache_raw = fetch_file('usercache.json')
    if not cache_raw:
        print("Failed to download usercache.json")
        return

    users = json.loads(cache_raw)
    print(f"Total users found in cache: {len(users)}")

    os.makedirs('data/players', exist_ok=True)
    with open('data/usercache.json', 'w', encoding='utf-8') as f:
        f.write(cache_raw)

    count = 0
    for u in users:
        uuid = u['uuid']
        name = u['name']
        print(f"[{count+1}/{len(users)}] Descargando datos de {name} ({uuid})...")
        
        stats = fetch_file(f"/world/players/stats/{uuid}.json")
        if stats:
            with open(f"data/players/{uuid}_stats.json", 'w', encoding='utf-8') as f:
                f.write(stats)
            print(f"  [OK] stats.json ({len(stats)} bytes)")
        else:
            print(f"  [-] No tiene stats.json")

        aura = fetch_file(f"/plugins/AuraSkills/userdata/{uuid}.yml")
        if aura:
            with open(f"data/players/{uuid}_auraskills.yml", 'w', encoding='utf-8') as f:
                f.write(aura)
            print(f"  [OK] auraskills.yml ({len(aura)} bytes)")
        else:
            print(f"  [-] No tiene auraskills.yml")

        adv = fetch_file(f"/world/players/advancements/{uuid}.json")
        if adv:
            with open(f"data/players/{uuid}_advancements.json", 'w', encoding='utf-8') as f:
                f.write(adv)
            print(f"  [OK] advancements.json ({len(adv)} bytes)")
        else:
            print(f"  [-] No tiene advancements.json")

        count += 1
        time.sleep(1)

    print("Sincronizacion completada con exito.")

if __name__ == '__main__':
    main()
