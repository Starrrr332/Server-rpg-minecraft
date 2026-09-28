import requests
import json

def check_db():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 HolyBot/1.0'
    }

    # 1. Query databases
    r = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/databases?include=password",
        headers=headers,
        timeout=15
    )
    print("Databases status:", r.status_code)
    if r.status_code == 200:
        d = r.json()
        items = d.get('data', [])
        print(f"Total databases found: {len(items)}")
        for db in items:
            attrs = db.get('attributes', {})
            print("  ID:", attrs.get('id'))
            print("  Name:", attrs.get('name'))
            host = attrs.get('host', {})
            print("  Host:", host.get('address'), ":", host.get('port'))
            print("  User:", attrs.get('username'))
            rel = attrs.get('relationships', {}).get('password', {}).get('attributes', {})
            pwd = rel.get('password')
            print("  Password available:", bool(pwd))
            if pwd:
                print("  Password:", pwd)
    else:
        print("Error query databases:", r.text[:300])

    # 2. List /plugins
    print("\n--- Listando /plugins ---")
    r_pl = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/list",
        headers=headers,
        params={'directory': '/plugins'},
        timeout=15
    )
    if r_pl.status_code == 200:
        for it in r_pl.json().get('data', []):
            print(" ", it['attributes']['name'])
    else:
        print("Error list plugins:", r_pl.status_code)

    # 3. Test creating database if 0 exist
    print("\n--- Probando creacion de base de datos SQL via API ---")
    payload = {"database": "mc_accounts", "remote": "%"}
    r_create = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/databases",
        headers=headers,
        json=payload,
        timeout=15
    )
    print("Create DB status:", r_create.status_code)
    if r_create.status_code in [200, 201]:
        print("Database creada exitosamente!")
        print(r_create.text[:400])
    else:
        print("Response:", r_create.text[:400])

if __name__ == '__main__':
    check_db()
