import requests
import json

with open("bot_config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {cfg['api_key']}", "Accept": "application/json"})

def list_dir(p):
    r = session.get(f"{base_url}/files/list", params={'directory': p}, timeout=10)
    if r.status_code == 200:
        return [item['attributes']['name'] for item in r.json().get('data', [])]
    return []

def get_file(p):
    r = session.get(f"{base_url}/files/contents", params={'file': p}, timeout=10)
    if r.status_code == 200:
        return r.text
    return None

def write_file(p, content):
    r = session.post(f"{base_url}/files/write", params={'file': p}, data=content.encode('utf-8'), timeout=10)
    return r.status_code

npc_files = list_dir("/plugins/EliteMobs/npcs")
print(f"Auditando {len(npc_files)} NPCs de EliteMobs para reparar mazmorras no descargadas...")

valid_dungeons = ["tier1_criptas.yml", "tier2_volcan.yml", "tier3_invierno.yml"]
replacements_count = 0

for f in npc_files:
    if not f.endswith(".yml"): continue
    path = f"/plugins/EliteMobs/npcs/{f}"
    content = get_file(path)
    if not content: continue

    lines = content.splitlines()
    modified = False
    new_lines = []

    for line in lines:
        if line.strip().startswith("command: em dungeontp"):
            parts = line.strip().split(" ")
            if len(parts) >= 3:
                target_dung = parts[2].strip()
                if target_dung not in valid_dungeons:
                    # Asignar una de las 3 mazmorras activas según tipo o tier
                    replacement_dung = "tier1_criptas.yml"
                    if "volcan" in f.lower() or "fire" in f.lower() or "dark" in f.lower() or "vampire" in f.lower():
                        replacement_dung = "tier2_volcan.yml"
                    elif "frost" in f.lower() or "ice" in f.lower() or "winter" in f.lower() or "invierno" in f.lower():
                        replacement_dung = "tier3_invierno.yml"

                    line = f"command: em dungeontp {replacement_dung}"
                    modified = True
                    replacements_count += 1
                    print(f"  [REPARADO] {f}: {target_dung} -> {replacement_dung}")

        new_lines.append(line)

    if modified:
        write_file(path, "\n".join(new_lines))

print(f"\n[EXITO] Se actualizaron {replacements_count} teletransportadores de mazmorras no instaladas hacia las mazmorras activas (Criptas, Volcán, Pico Helado)!")
