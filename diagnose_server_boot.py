import requests
import json
import time

with open("bot_config.json", "r") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
headers = {
    "Authorization": f"Bearer {cfg['api_key']}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

r = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
if r.status_code == 200:
    data = r.json().get('attributes', {})
    print("RECURSOS DEL SERVIDOR:")
    print("  State:", data.get('current_state'))
    print("  is_running:", data.get('is_running'))
    res = data.get('resources', {})
    print("  Memory:", res.get('memory_bytes', 0) / (1024*1024), "MB")
    print("  CPU Absolute:", res.get('cpu_absolute'), "%")
    print("  Disk:", res.get('disk_bytes', 0) / (1024*1024), "MB")
else:
    print("Error recursos:", r.status_code, r.text)

# Intentar mandar un comando de consola
r_cmd = requests.post(f"{base_url}/command", headers=headers, json={"command": "list"}, timeout=10)
print("Envío de comando 'list':", r_cmd.status_code)

time.sleep(2)

r_log = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'logs/latest.log'}, timeout=10)
if r_log.status_code == 200:
    lines = r_log.text.splitlines()
    print(f"\n--- ÚLTIMAS 15 LÍNEAS DE LOG (Total {len(lines)}) ---")
    for l in lines[-15:]:
        print(l)
