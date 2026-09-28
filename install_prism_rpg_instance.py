import os
import shutil
import json
import urllib.request
import time

PRISM_DIR = "C:/Users/amaro/Downloads/Prism Launcher"
INSTANCES_DIR = os.path.join(PRISM_DIR, "instances")
NEW_INST_DIR = os.path.join(INSTANCES_DIR, "Holy RPG 26.2 (Fabric)")
KEO_INST_DIR = os.path.join(INSTANCES_DIR, "Keo optimized(1)")

print("=== CREANDO INSTANCIA PERSONALIZADA PARA PRISM LAUNCHER ===")
print(f"Destino: {NEW_INST_DIR}")

# 1. Crear directorios base
minecraft_dir = os.path.join(NEW_INST_DIR, "minecraft")
mods_dir = os.path.join(minecraft_dir, "mods")
config_dir = os.path.join(minecraft_dir, "config")
resourcepacks_dir = os.path.join(minecraft_dir, "resourcepacks")

os.makedirs(mods_dir, exist_ok=True)
os.makedirs(config_dir, exist_ok=True)
os.makedirs(resourcepacks_dir, exist_ok=True)

# 2. Configurar instance.cfg
instance_cfg_content = """[General]
InstanceType=OneSix
iconKey=sword
name=Holy RPG 26.2 (Fabric)
ConfigVersion=1.3
AutomaticJava=true
JavaArchitecture=64
JavaRealArchitecture=amd64
LogPrePostOutput=true
ManagedPack=false
JoinServerOnLaunch=false
OverrideJavaLocation=true
JavaPath=C:/Users/amaro/Downloads/Prism Launcher/java/java-runtime-epsilon/bin/javaw.exe
JavaVersion=25.0.1
OverrideMemory=true
MinMemAlloc=1024
MaxMemAlloc=4096
notes=Modpack Client-Side RPG Oficial para Holy Server (Minecraft 26.2 Fabric). Incluye RPG-HUD, barras de vida flotantes Provi, Minimapa y Mapa Mundial Fair-Play de Xaero, Crosshair Dinamico, Sonido Espacial 3D, Presencia de Pisadas y el paquete de interfaz Mandala GUI Dark Mode.
"""
with open(os.path.join(NEW_INST_DIR, "instance.cfg"), "w", encoding="utf-8") as f:
    f.write(instance_cfg_content)

# 3. Configurar mmc-pack.json
mmc_pack_content = {
    "components": [
        {
            "cachedName": "LWJGL 3",
            "cachedVersion": "3.4.1",
            "cachedVolatile": True,
            "dependencyOnly": True,
            "uid": "org.lwjgl3",
            "version": "3.4.1"
        },
        {
            "cachedName": "Minecraft",
            "cachedRequires": [
                {
                    "suggests": "3.4.1",
                    "uid": "org.lwjgl3"
                }
            ],
            "cachedVersion": "26.2",
            "important": True,
            "uid": "net.minecraft",
            "version": "26.2"
        },
        {
            "cachedName": "Intermediary Mappings",
            "cachedRequires": [
                {
                    "equals": "26.2",
                    "uid": "net.minecraft"
                }
            ],
            "cachedVersion": "26.2",
            "cachedVolatile": True,
            "dependencyOnly": True,
            "uid": "net.fabricmc.intermediary",
            "version": "26.2"
        },
        {
            "cachedName": "Fabric Loader",
            "cachedRequires": [
                {
                    "uid": "net.fabricmc.intermediary"
                }
            ],
            "cachedVersion": "0.19.3",
            "uid": "net.fabricmc.fabric-loader",
            "version": "0.19.3"
        }
    ],
    "formatVersion": 1
}
with open(os.path.join(NEW_INST_DIR, "mmc-pack.json"), "w", encoding="utf-8") as f:
    json.dump(mmc_pack_content, f, indent=4)

# 4. Copiar mods base de optimización y motor Fabric 26.2 desde Keo optimized(1)
print("\n[1/4] Copiando motor y optimizaciones de 26.2 desde Keo optimized(1)...")
keo_mods_dir = os.path.join(KEO_INST_DIR, "minecraft", "mods")
if os.path.exists(keo_mods_dir):
    for f in os.listdir(keo_mods_dir):
        if not f.endswith(".jar"):
            continue
        src = os.path.join(keo_mods_dir, f)
        dst = os.path.join(mods_dir, f)
        shutil.copy2(src, dst)
        print(f"  + Motor: {f}")

# 5. Descargar mods RPG para 26.2 desde Modrinth
rpg_mods_26 = [
    "rpg-hud",
    "provis-health-bars",
    "xaeros-minimap",
    "xaeros-world-map",
    "dynamiccrosshair",
    "appleskin",
    "not-enough-animations",
    "3dskinlayers",
    "wavey-capes",
    "inventory-profiles-next",
    "shulkerboxtooltip",
    "lambdynamiclights",
    "sound-physics-remastered",
    "presence-footsteps"
]

print(f"\n[2/4] Descargando {len(rpg_mods_26)} mods RPG para 26.2...")
for slug in rpg_mods_26:
    url = f"https://api.modrinth.com/v2/project/{slug}/version?loaders=[%22fabric%22]"
    req = urllib.request.Request(url, headers={"User-Agent": "HolyServer-PrismInstaller/1.0"})
    try:
        with urllib.request.urlopen(req) as res:
            versions = json.loads(res.read().decode("utf-8"))
            m26 = [x for x in versions if any("26.2" in gv for gv in x.get("game_versions", []))]
            if m26:
                top_v = m26[0]
                primary_file = next((f for f in top_v["files"] if f.get("primary")), top_v["files"][0])
                fn = primary_file["filename"]
                dl_url = primary_file["url"]
                target_path = os.path.join(mods_dir, fn)
                if not os.path.exists(target_path):
                    print(f"  + Descargando {slug} -> {fn}...")
                    urllib.request.urlretrieve(dl_url, target_path)
                else:
                    print(f"  = Ya presente: {fn}")
            else:
                print(f"  ! Sin version 26.2 directa para {slug}")
        time.sleep(0.12)
    except Exception as e:
        print(f"  x Error con {slug}: {e}")

# 6. Copiar Resource Pack (Mandala GUI Dark Mode)
print("\n[3/4] Instalando Resource Pack Mandala GUI Dark Mode...")
rp_src = "c:/Users/amaro/OneDrive/Desktop/Bot para server/modpack_rpg_client/resourcepacks/MandalasGUI_DarkMode_1.21.zip"
rp_dst = os.path.join(resourcepacks_dir, "MandalasGUI_DarkMode.zip")
if os.path.exists(rp_src):
    shutil.copy2(rp_src, rp_dst)
    print("  + Mandala's GUI Dark Mode instalado en resourcepacks/")

# 7. Copiar y generar configuraciones de interfaz
print("\n[4/4] Aplicando configuraciones de interfaz y multiplayer...")
cfg_src = "c:/Users/amaro/OneDrive/Desktop/Bot para server/modpack_rpg_client/config"
if os.path.exists(cfg_src):
    for f in os.listdir(cfg_src):
        shutil.copy2(os.path.join(cfg_src, f), os.path.join(config_dir, f))
        print(f"  + Config: {f}")

# Copiar servers.dat y options.txt desde 26.2 para que ya tenga Holy Server y pantalla completa configurados
source_options = "C:/Users/amaro/Downloads/Prism Launcher/instances/26.2/minecraft/options.txt"
source_servers = "C:/Users/amaro/Downloads/Prism Launcher/instances/26.2/minecraft/servers.dat"

if os.path.exists(source_servers):
    shutil.copy2(source_servers, os.path.join(minecraft_dir, "servers.dat"))
    print("  + Servidor Holy Server (suuup.holy.gg) copiado a servers.dat")

if os.path.exists(source_options):
    shutil.copy2(source_options, os.path.join(minecraft_dir, "options.txt"))
    print("  + Opciones graficas personalizadas copiadas a options.txt")

total_mods = len([f for f in os.listdir(mods_dir) if f.endswith(".jar")])
print(f"\n=== INSTALACION EXITOSA ===")
print(f"Instancia creada: '{NEW_INST_DIR}'")
print(f"Total de mods instalados: {total_mods}")
