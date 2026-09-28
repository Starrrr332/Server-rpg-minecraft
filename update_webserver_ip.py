import requests
import json

def update_webserver():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0'
    }

    # 1. Read webserver.conf
    r = requests.get(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/contents",
        headers=headers,
        params={'file': '/plugins/BlueMap/webserver.conf'},
        timeout=15
    )
    if r.status_code != 200:
        print("Error reading webserver.conf:", r.status_code)
        return

    content = r.text
    if 'ip: "0.0.0.0"' not in content:
        # insert ip: "0.0.0.0" right above port: 25898
        new_content = content.replace("port: 25898", "ip: \"0.0.0.0\"\nport: 25898")
        print("Agregando ip: \"0.0.0.0\" a webserver.conf...")
        
        # Write back
        write_url = f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/files/write?file=/plugins/BlueMap/webserver.conf"
        r_w = requests.post(
            write_url,
            headers={**headers, 'Content-Type': 'application/octet-stream'},
            data=new_content.encode('utf-8'),
            timeout=20
        )
        print("Status escritura:", r_w.status_code)
    else:
        print("ip: \"0.0.0.0\" ya estaba presente.")

if __name__ == '__main__':
    update_webserver()
