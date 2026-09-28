import json
import os

config_dir = "modpack_rpg_client/config"
os.makedirs(config_dir, exist_ok=True)

# 1. Equipment Compare config
eq_config = {
    "showComparison": True,
    "requireShift": True,
    "showDifferenceInTooltip": True,
    "highlightBetterAttributes": True,
    "highlightWorseAttributes": True,
    "betterAttributeColor": "GREEN",
    "worseAttributeColor": "RED",
    "equalAttributeColor": "YELLOW",
    "compareBaubles": True,
    "compareMainhand": True,
    "compareOffhand": True
}
with open(os.path.join(config_dir, "equipmentcompare.json"), "w", encoding="utf-8") as f:
    json.dump(eq_config, f, indent=2)

# 2. Traveler's Titles config (Elden Ring / Souls-like biome banner)
tt_config = {
    "displayTime": 80,
    "fadeInTime": 20,
    "fadeOutTime": 20,
    "titleColor": "#E6C280",
    "subtitleColor": "#B0A898",
    "playSound": True,
    "soundVolume": 0.8,
    "showSubtitles": True,
    "minDistanceBetweenTitles": 64,
    "renderStyle": "ELDEN_DARK"
}
with open(os.path.join(config_dir, "travelerstitles.json"), "w", encoding="utf-8") as f:
    json.dump(tt_config, f, indent=2)

# 3. Sound Physics Remastered config
sp_config = {
    "master_volume": 1.0,
    "reverb_gain": 0.85,
    "reverb_brightness": 0.95,
    "occlusion_factor": 0.8,
    "distance_attenuation": 1.0,
    "air_absorption": 0.05,
    "enable_cave_reverb": True,
    "enable_water_muffling": True
}
with open(os.path.join(config_dir, "sound_physics.json"), "w", encoding="utf-8") as f:
    json.dump(sp_config, f, indent=2)

# 4. Provi's Health Bars config
provi_config = {
    "showMobHealth": True,
    "showPlayerHealth": True,
    "showBossHealth": True,
    "showDamageNumbers": True,
    "barStyle": "RPG_FLUID",
    "renderDistance": 32,
    "showAbsorption": True,
    "showStatusEffects": True,
    "eliteMobHighlight": True
}
with open(os.path.join(config_dir, "provihealth.json"), "w", encoding="utf-8") as f:
    json.dump(provi_config, f, indent=2)

# 5. Dynamic Crosshair config
dc_config = {
    "style": "DYNAMIC_RPG",
    "hideOnCinematic": True,
    "highlightHostiles": True,
    "hostileColor": "#E74C3C",
    "chestColor": "#F39C12",
    "friendlyColor": "#2ECC71",
    "showCooldown": True
}
with open(os.path.join(config_dir, "dynamiccrosshair.json"), "w", encoding="utf-8") as f:
    json.dump(dc_config, f, indent=2)

print("Preset configuration files created successfully in config/!")
