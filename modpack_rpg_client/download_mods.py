import os
import json
import urllib.request
import zipfile
import time

TARGET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mods')
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
RESOURCEPACK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resourcepacks')

os.makedirs(TARGET_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(RESOURCEPACK_DIR, exist_ok=True)

mods_to_download = [
    {"slug": "fabric-api", "category": "Core"},
    {"slug": "modmenu", "category": "Core"},
    {"slug": "cloth-config", "category": "Core / Dependencia"},
    {"slug": "yacl", "category": "Core / Dependencia"},
    {"slug": "fabric-language-kotlin", "category": "Core / Dependencia"},
    {"slug": "libipn", "category": "Core / Dependencia"},
    {"slug": "kirin", "category": "Core / Dependencia"},
    {"slug": "rpg-hud", "category": "RPG HUD & Interfaz"},
    {"slug": "provis-health-bars", "category": "Combate & Indicadores"},
    {"slug": "equipment-compare", "category": "RPG HUD & Interfaz"},
    {"slug": "xaeros-minimap", "category": "Mapas & Navegación"},
    {"slug": "xaeros-world-map", "category": "Mapas & Navegación"},
    {"slug": "travelers-titles", "category": "Animaciones & Inmersión"},
    {"slug": "dynamiccrosshair", "category": "RPG HUD & Interfaz"},
    {"slug": "appleskin", "category": "RPG HUD & Interfaz"},
    {"slug": "not-enough-animations", "category": "Animaciones & Inmersión"},
    {"slug": "3dskinlayers", "category": "Animaciones & Inmersión"},
    {"slug": "wavey-capes", "category": "Animaciones & Inmersión"},
    {"slug": "inventory-profiles-next", "category": "Calidad de Vida"},
    {"slug": "shulkerboxtooltip", "category": "Calidad de Vida"},
    {"slug": "sodium", "category": "Rendimiento & Shaders"},
    {"slug": "iris", "category": "Rendimiento & Shaders"},
    {"slug": "immediatelyfast", "category": "Rendimiento & Shaders"},
    {"slug": "ferrite-core", "category": "Rendimiento & Shaders"},
    {"slug": "lambdynamiclights", "category": "Iluminación & Inmersión"},
    {"slug": "sound-physics-remastered", "category": "Sonido & Atmósfera"},
    {"slug": "presence-footsteps", "category": "Sonido & Atmósfera"}
]

print(f"=== INICIANDO DESCARGA DE MODS CLIENT-SIDE PARA FABRIC 1.21.1 ({len(mods_to_download)} MODS) ===")
downloaded_count = 0
failed_mods = []

for mod_info in mods_to_download:
    slug = mod_info["slug"]
    url = f"https://api.modrinth.com/v2/project/{slug}/version?loaders=[%22fabric%22]"
    req = urllib.request.Request(url, headers={"User-Agent": "HolyServer-Modpack-Downloader/1.0"})
    try:
        with urllib.request.urlopen(req) as res:
            versions = json.loads(res.read().decode("utf-8"))
            match = [v for v in versions if "1.21.1" in v.get("game_versions", [])]
            if not match:
                match = [v for v in versions if "1.21" in v.get("game_versions", [])]
            if not match:
                match = [v for v in versions if any(gv.startswith("1.21") for gv in v.get("game_versions", []))]

            if match:
                top_v = match[0]
                primary_file = next((f for f in top_v["files"] if f.get("primary")), top_v["files"][0])
                filename = primary_file["filename"]
                download_url = primary_file["url"]
                target_file_path = os.path.join(TARGET_DIR, filename)

                if not os.path.exists(target_file_path):
                    print(f"Descargando {slug} -> {filename}...")
                    urllib.request.urlretrieve(download_url, target_file_path)
                else:
                    print(f"[YA EXISTE] {filename}")
                downloaded_count += 1
            else:
                print(f"[ERROR] No compatible version found for {slug}")
                failed_mods.append(slug)
        time.sleep(0.12)
    except Exception as e:
        print(f"[ERROR al descargar {slug}]: {e}")
        failed_mods.append(slug)

print(f"\nDescarga finalizada: {downloaded_count}/{len(mods_to_download)} mods descargados exitosamente.")
if failed_mods:
    print(f"Mods que fallaron: {failed_mods}")
