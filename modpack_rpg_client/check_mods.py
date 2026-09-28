import urllib.request
import json
import time

manifest = json.load(open('modpack_rpg_client/modpack_manifest.json', 'r', encoding='utf-8'))
results = {}

for mod in manifest['mods']:
    slug = mod['slug']
    url = f'https://api.modrinth.com/v2/project/{slug}/version?loaders=[%22fabric%22]'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'HolyServer-Modpack-Checker/1.0'})
        with urllib.request.urlopen(req) as res:
            versions = json.loads(res.read().decode('utf-8'))
            # Filter for 1.21.x
            v121 = [v for v in versions if any(gv.startswith('1.21') for gv in v.get('game_versions', []))]
            if v121:
                top_v = v121[0]
                primary_file = next((f for f in top_v['files'] if f.get('primary')), top_v['files'][0])
                results[slug] = {
                    'status': 'OK',
                    'filename': primary_file['filename'],
                    'url': primary_file['url'],
                    'mc_versions': top_v['game_versions'],
                    'dependencies': top_v.get('dependencies', [])
                }
                print(f"[OK] {slug} -> {primary_file['filename']}")
            else:
                results[slug] = {'status': 'NOT_FOUND_1.21'}
                print(f"[MISSING 1.21] {slug}")
        time.sleep(0.15)
    except Exception as e:
        results[slug] = {'status': 'ERROR', 'error': str(e)}
        print(f"[ERROR] {slug}: {e}")

with open('modpack_rpg_client/mod_check_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
print("Finished checking mods.")
