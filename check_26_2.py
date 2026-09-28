import urllib.request
import json

slugs = [
    'rpg-hud', 'provis-health-bars', 'equipment-compare',
    'xaeros-minimap', 'xaeros-world-map', 'travelers-titles',
    'dynamiccrosshair', 'appleskin', 'not-enough-animations',
    '3dskinlayers', 'wavey-capes', 'inventory-profiles-next',
    'shulkerboxtooltip', 'lambdynamiclights', 'sound-physics-remastered',
    'presence-footsteps'
]

print("=== CHECKING MODRINTH FOR MINECRAFT 26.2 ===")
for slug in slugs:
    url = f'https://api.modrinth.com/v2/project/{slug}/version?loaders=[%22fabric%22]'
    req = urllib.request.Request(url, headers={'User-Agent': 'HolyServer/1.0'})
    try:
        with urllib.request.urlopen(req) as res:
            v = json.loads(res.read().decode('utf-8'))
            m26 = [x for x in v if any('26.2' in gv for gv in x.get('game_versions', []))]
            if m26:
                fn = m26[0]['files'][0]['filename']
                print(f"[26.2 MATCH] {slug:25}: {fn}")
            else:
                top_v = v[0] if v else None
                top_gv = top_v['game_versions'][0] if top_v else 'None'
                print(f"[NO 26.2]   {slug:25}: latest is {top_gv}")
    except Exception as e:
        print(f"[ERR] {slug}: {e}")
