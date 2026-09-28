# -*- coding: utf-8 -*-
import os
import json
import re

# Comprehensive Minecraft ID translations to Spanish
SPANISH_TRANSLATIONS = {
    # Mobs
    "minecraft:zombie": "Zombi",
    "minecraft:skeleton": "Esqueleto",
    "minecraft:creeper": "Creeper",
    "minecraft:spider": "Araña",
    "minecraft:cave_spider": "Araña de cueva",
    "minecraft:enderman": "Enderman",
    "minecraft:drowned": "Ahogado",
    "minecraft:husk": "Momia / Husk",
    "minecraft:stray": "Vagabundo",
    "minecraft:witch": "Bruja",
    "minecraft:phantom": "Fantasma",
    "minecraft:slime": "Slime",
    "minecraft:magma_cube": "Cubo de magma",
    "minecraft:blaze": "Blaze",
    "minecraft:ghast": "Ghast",
    "minecraft:wither_skeleton": "Esqueleto Wither",
    "minecraft:piglin": "Piglin",
    "minecraft:zombified_piglin": "Piglin Zombificado",
    "minecraft:piglin_brute": "Piglin Bruto",
    "minecraft:hoglin": "Hoglin",
    "minecraft:zoglin": "Zoglin",
    "minecraft:pillager": "Saqueador",
    "minecraft:vindicator": "Vindicador",
    "minecraft:evoker": "Evocador",
    "minecraft:ravager": "Devastador",
    "minecraft:vex": "Vex",
    "minecraft:guardian": "Guardián",
    "minecraft:elder_guardian": "Guardián Anciano",
    "minecraft:shulker": "Shulker",
    "minecraft:silverfish": "Lepisma",
    "minecraft:endermite": "Endermite",
    "minecraft:warden": "Warden",
    "minecraft:ender_dragon": "Dragón del Fin",
    "minecraft:wither": "Wither",
    "minecraft:breeze": "Breeze",
    "minecraft:bogged": "Enlodado (Bogged)",
    "minecraft:cow": "Vaca",
    "minecraft:sheep": "Oveja",
    "minecraft:pig": "Cerdo",
    "minecraft:chicken": "Pollo",
    "minecraft:horse": "Caballo",
    "minecraft:donkey": "Burro",
    "minecraft:mule": "Mula",
    "minecraft:iron_golem": "Gólem de hierro",
    "minecraft:snow_golem": "Gólem de nieve",
    "minecraft:villager": "Aldeano",
    "minecraft:wandering_trader": "Vendedor Ambulante",
    "minecraft:wolf": "Lobo",
    "minecraft:cat": "Gato",
    "minecraft:ocelot": "Ocelote",
    "minecraft:bat": "Murciélago",
    "minecraft:parrot": "Loro",
    "minecraft:bee": "Abeja",
    "minecraft:fox": "Zorro",
    "minecraft:polar_bear": "Oso Polar",
    "minecraft:panda": "Panda",
    "minecraft:strider": "Lavagante",
    "minecraft:squid": "Calamar",
    "minecraft:glow_squid": "Calamar Brillante",
    "minecraft:dolphin": "Delfín",
    "minecraft:turtle": "Tortuga",
    "minecraft:axolotl": "Ajolote",
    "minecraft:frog": "Rana",
    "minecraft:allay": "Allay",
    "minecraft:camel": "Camello",
    "minecraft:armadillo": "Armadillo",
    "minecraft:sniffer": "Sniffer",

    # Blocks and Items
    "minecraft:stone": "Piedra",
    "minecraft:cobblestone": "Adoquín",
    "minecraft:deepslate": "Pizarra profunda",
    "minecraft:cobbled_deepslate": "Adoquín de pizarra profunda",
    "minecraft:dirt": "Tierra",
    "minecraft:grass_block": "Bloque de pasto",
    "minecraft:sand": "Arena",
    "minecraft:gravel": "Grava",
    "minecraft:coal_ore": "Mineral de carbón",
    "minecraft:deepslate_coal_ore": "Mineral de carbón de pizarra",
    "minecraft:iron_ore": "Mineral de hierro",
    "minecraft:deepslate_iron_ore": "Mineral de hierro de pizarra",
    "minecraft:copper_ore": "Mineral de cobre",
    "minecraft:deepslate_copper_ore": "Mineral de cobre de pizarra",
    "minecraft:gold_ore": "Mineral de oro",
    "minecraft:deepslate_gold_ore": "Mineral de oro de pizarra",
    "minecraft:redstone_ore": "Mineral de redstone",
    "minecraft:deepslate_redstone_ore": "Mineral de redstone de pizarra",
    "minecraft:lapis_ore": "Mineral de lapislázuli",
    "minecraft:deepslate_lapis_ore": "Mineral de lapislázuli de pizarra",
    "minecraft:diamond_ore": "Mineral de diamante",
    "minecraft:deepslate_diamond_ore": "Mineral de diamante de pizarra",
    "minecraft:emerald_ore": "Mineral de esmeralda",
    "minecraft:deepslate_emerald_ore": "Mineral de esmeralda de pizarra",
    "minecraft:nether_quartz_ore": "Mineral de cuarzo del Nether",
    "minecraft:nether_gold_ore": "Mineral de oro del Nether",
    "minecraft:ancient_debris": "Escombros ancestrales (Netherite)",
    "minecraft:oak_log": "Tronco de roble",
    "minecraft:birch_log": "Tronco de abedul",
    "minecraft:spruce_log": "Tronco de abeto",
    "minecraft:jungle_log": "Tronco de jungla",
    "minecraft:acacia_log": "Tronco de acacia",
    "minecraft:dark_oak_log": "Tronco de roble oscuro",
    "minecraft:mangrove_log": "Tronco de mangle",
    "minecraft:cherry_log": "Tronco de cerezo",
    "minecraft:obsidian": "Obsidiana",
    "minecraft:crying_obsidian": "Obsidiana llorosa",
    "minecraft:torch": "Antorcha",
    "minecraft:crafting_table": "Mesa de crafteo",
    "minecraft:furnace": "Horno",
    "minecraft:chest": "Cofre",
    "minecraft:barrel": "Barril",
    "minecraft:shulker_box": "Caja de Shulker",
    "minecraft:diamond_pickaxe": "Pico de diamante",
    "minecraft:netherite_pickaxe": "Pico de inframundita",
    "minecraft:iron_pickaxe": "Pico de hierro",
    "minecraft:diamond_sword": "Espada de diamante",
    "minecraft:netherite_sword": "Espada de inframundita",
    "minecraft:iron_sword": "Espada de hierro",
    "minecraft:bow": "Arco",
    "minecraft:crossbow": "Ballesta",
    "minecraft:trident": "Tridente",
    "minecraft:shield": "Escudo",
    "minecraft:golden_apple": "Manzana dorada",
    "minecraft:enchanted_golden_apple": "Manzana dorada encantada",
    "minecraft:ender_pearl": "Perla de Ender",
    "minecraft:bread": "Pan",
    "minecraft:cooked_beef": "Bife cocinado",
    "minecraft:cooked_porkchop": "Chuleta de cerdo cocinada",
    "minecraft:cooked_mutton": "Carne de cordero cocinada"
}

SKILL_NAMES_ES = {
    "auraskills/fishing": "Pesca",
    "auraskills/fighting": "Combate",
    "auraskills/alchemy": "Alquimia",
    "auraskills/farming": "Agricultura",
    "auraskills/agility": "Agilidad",
    "auraskills/excavation": "Excavación",
    "auraskills/foraging": "Tala / Recolección",
    "auraskills/archery": "Tiro con arco",
    "auraskills/mining": "Minería",
    "auraskills/defense": "Defensa",
    "auraskills/enchanting": "Encantamiento"
}

SKILL_ICONS = {
    "auraskills/fishing": "🎣",
    "auraskills/fighting": "⚔️",
    "auraskills/alchemy": "🧪",
    "auraskills/farming": "🌾",
    "auraskills/agility": "⚡",
    "auraskills/excavation": "⛏️",
    "auraskills/foraging": "🪓",
    "auraskills/archery": "🏹",
    "auraskills/mining": "💎",
    "auraskills/defense": "🛡️",
    "auraskills/enchanting": "✨"
}

def translate_id(item_id):
    if not item_id:
        return ""
    if item_id in SPANISH_TRANSLATIONS:
        return SPANISH_TRANSLATIONS[item_id]
    cleaned = item_id.replace("minecraft:", "").replace("_", " ")
    return cleaned.title()

def parse_yaml_simple(text):
    data = {}
    skills = {}
    current_skill = None
    in_skills = False
    for line in text.splitlines():
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('skills:'):
            in_skills = True
            current_skill = None
            continue
        elif not line.startswith(' ') and ':' in line:
            in_skills = False
            parts = line.split(':', 1)
            k = parts[0].strip()
            v = parts[1].strip()
            if k == 'uuid':
                data['uuid'] = v
            elif k == 'mana':
                try:
                    data['mana'] = float(v)
                except:
                    data['mana'] = 0.0
            continue
        
        if in_skills:
            if line.startswith('  auraskills/'):
                current_skill = line.split(':', 1)[0].strip()
                skills[current_skill] = {'level': 0, 'xp': 0.0}
            elif current_skill and 'level:' in line:
                try:
                    skills[current_skill]['level'] = int(line.split(':', 1)[1].strip())
                except:
                    pass
            elif current_skill and 'xp:' in line:
                try:
                    skills[current_skill]['xp'] = float(line.split(':', 1)[1].strip())
                except:
                    pass
    data['skills'] = skills
    return data

def build_player_data(uuid, name):
    stats_file = f"data/players/{uuid}_stats.json"
    aura_file = f"data/players/{uuid}_auraskills.yml"
    adv_file = f"data/players/{uuid}_advancements.json"

    # Default structure
    player = {
        "uuid": uuid,
        "name": name,
        "is_bedrock": name.startswith('.'),
        "avatar": f"https://mc-heads.net/avatar/{uuid}/100" if not name.startswith('.') else f"https://minotar.net/helm/{name}/100.png",
        "bust": f"https://mc-heads.net/bust/{uuid}/160" if not name.startswith('.') else f"https://minotar.net/bust/{name}/160.png",
        "play_time_seconds": 0,
        "play_time_str": "0m",
        "deaths": 0,
        "mob_kills": 0,
        "player_kills": 0,
        "kdr": 0.0,
        "damage_dealt": 0,
        "damage_taken": 0,
        "jumps": 0,
        "distances": {
            "walk_km": 0.0,
            "sprint_km": 0.0,
            "fly_km": 0.0,
            "boat_km": 0.0,
            "horse_km": 0.0,
            "total_km": 0.0
        },
        "total_mined": 0,
        "total_crafted": 0,
        "total_picked_up": 0,
        "skills": [],
        "total_skill_level": 0,
        "skill_average": 0.0,
        "mana": 0.0,
        "advancements_count": 0,
        "advancements": [],
        "top_mined": [],
        "top_crafted": [],
        "top_mobs_killed": [],
        "deaths_by": []
    }

    # Load stats.json
    if os.path.exists(stats_file):
        try:
            with open(stats_file, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            stats = raw.get('stats', {})
            custom = stats.get('minecraft:custom', {})

            ticks = custom.get('minecraft:play_time', 0)
            seconds = ticks // 20
            player['play_time_seconds'] = seconds
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            mins = (seconds % 3600) // 60
            if days > 0:
                player['play_time_str'] = f"{days}d {hours}h {mins}m"
            elif hours > 0:
                player['play_time_str'] = f"{hours}h {mins}m"
            else:
                player['play_time_str'] = f"{mins}m"

            player['deaths'] = custom.get('minecraft:deaths', 0)
            player['mob_kills'] = custom.get('minecraft:mob_kills', 0)
            player['player_kills'] = custom.get('minecraft:player_kills', 0)
            player['damage_dealt'] = round(custom.get('minecraft:damage_dealt', 0) / 20) # Corazones
            player['damage_taken'] = round(custom.get('minecraft:damage_taken', 0) / 20)
            player['jumps'] = custom.get('minecraft:jump', 0)

            # KDR
            player['kdr'] = round(player['mob_kills'] / max(1, player['deaths']), 2)

            # Distances
            w_cm = custom.get('minecraft:walk_one_cm', 0)
            s_cm = custom.get('minecraft:sprint_one_cm', 0)
            f_cm = custom.get('minecraft:fly_one_cm', 0)
            b_cm = custom.get('minecraft:boat_one_cm', 0)
            h_cm = custom.get('minecraft:horse_one_cm', 0)

            player['distances']['walk_km'] = round(w_cm / 100000, 2)
            player['distances']['sprint_km'] = round(s_cm / 100000, 2)
            player['distances']['fly_km'] = round(f_cm / 100000, 2)
            player['distances']['boat_km'] = round(b_cm / 100000, 2)
            player['distances']['horse_km'] = round(h_cm / 100000, 2)
            player['distances']['total_km'] = round((w_cm + s_cm + f_cm + b_cm + h_cm) / 100000, 2)

            # Top Mined
            mined = stats.get('minecraft:mined', {})
            player['total_mined'] = sum(mined.values())
            sorted_mined = sorted(mined.items(), key=lambda x: x[1], reverse=True)[:10]
            player['top_mined'] = [{"id": k, "name": translate_id(k), "count": v} for k, v in sorted_mined]

            # Top Crafted
            crafted = stats.get('minecraft:crafted', {})
            player['total_crafted'] = sum(crafted.values())
            sorted_crafted = sorted(crafted.items(), key=lambda x: x[1], reverse=True)[:10]
            player['top_crafted'] = [{"id": k, "name": translate_id(k), "count": v} for k, v in sorted_crafted]

            # Top Picked Up
            picked = stats.get('minecraft:picked_up', {})
            player['total_picked_up'] = sum(picked.values())

            # Top Mobs Killed
            killed = stats.get('minecraft:killed', {})
            sorted_killed = sorted(killed.items(), key=lambda x: x[1], reverse=True)[:10]
            player['top_mobs_killed'] = [{"id": k, "name": translate_id(k), "count": v} for k, v in sorted_killed]

            # Killed by
            killed_by = stats.get('minecraft:killed_by', {})
            sorted_killed_by = sorted(killed_by.items(), key=lambda x: x[1], reverse=True)[:10]
            player['deaths_by'] = [{"id": k, "name": translate_id(k), "count": v} for k, v in sorted_killed_by]

        except Exception as e:
            print(f"Error parsing stats for {name}: {e}")

    # Load AuraSkills
    if os.path.exists(aura_file):
        try:
            with open(aura_file, 'r', encoding='utf-8') as f:
                ytext = f.read()
            ydata = parse_yaml_simple(ytext)
            player['mana'] = ydata.get('mana', 0.0)
            skills_dict = ydata.get('skills', {})
            tot_lvl = 0
            skill_list = []
            for s_id, s_name in SKILL_NAMES_ES.items():
                s_info = skills_dict.get(s_id, {"level": 0, "xp": 0.0})
                tot_lvl += s_info["level"]
                skill_list.append({
                    "id": s_id,
                    "name": s_name,
                    "icon": SKILL_ICONS.get(s_id, "✨"),
                    "level": s_info["level"],
                    "xp": round(s_info["xp"], 1)
                })
            player['skills'] = skill_list
            player['total_skill_level'] = tot_lvl
            player['skill_average'] = round(tot_lvl / max(1, len(SKILL_NAMES_ES)), 1)
        except Exception as e:
            print(f"Error parsing auraskills for {name}: {e}")

    # Load Advancements
    if os.path.exists(adv_file):
        try:
            with open(adv_file, 'r', encoding='utf-8') as f:
                adv_raw = json.load(f)
            adv_done = []
            for k, val in adv_raw.items():
                if isinstance(val, dict) and val.get('done') and not k.startswith('minecraft:recipes/'):
                    adv_done.append(k)
            player['advancements_count'] = len(adv_done)
            # Store some clean titles
            clean_adv = []
            for a in adv_done[:20]:
                title = a.replace('minecraft:', '').replace('_', ' ').replace('/', ' ▸ ')
                clean_adv.append(title.title())
            player['advancements'] = clean_adv
        except Exception as e:
            print(f"Error parsing advancements for {name}: {e}")

    return player

def build_database():
    cache_path = 'data/usercache.json'
    if not os.path.exists(cache_path):
        print("data/usercache.json does not exist yet.")
        return

    with open(cache_path, 'r', encoding='utf-8') as f:
        users = json.load(f)

    players = []
    for u in users:
        p = build_player_data(u['uuid'], u['name'])
        # only keep if player has some stats or playtime
        players.append(p)

    # Sort players by playtime or activity
    players.sort(key=lambda x: x['play_time_seconds'], reverse=True)

    # Calculate Leaderboards
    leaderboards = {
        "play_time": sorted(players, key=lambda x: x['play_time_seconds'], reverse=True)[:10],
        "auraskills": sorted(players, key=lambda x: (x['total_skill_level'], x['skill_average']), reverse=True)[:10],
        "mob_kills": sorted(players, key=lambda x: x['mob_kills'], reverse=True)[:10],
        "player_kills": sorted(players, key=lambda x: x['player_kills'], reverse=True)[:10],
        "mined": sorted(players, key=lambda x: x['total_mined'], reverse=True)[:10],
        "crafted": sorted(players, key=lambda x: x['total_crafted'], reverse=True)[:10],
        "distance": sorted(players, key=lambda x: x['distances']['total_km'], reverse=True)[:10],
        "kdr": sorted([p for p in players if p['deaths'] > 0 or p['mob_kills'] > 0], key=lambda x: x['kdr'], reverse=True)[:10]
    }

    # Summary
    server_summary = {
        "total_players": len(players),
        "total_play_time_hours": round(sum(p['play_time_seconds'] for p in players) / 3600, 1),
        "total_blocks_mined": sum(p['total_mined'] for p in players),
        "total_mobs_slain": sum(p['mob_kills'] for p in players),
        "total_distance_km": round(sum(p['distances']['total_km'] for p in players), 1),
        "server_ip": "ut09.holy.gg:25898",
        "map_url": "http://ut09.holy.gg:25898/"
    }

    output = {
        "summary": server_summary,
        "leaderboards": {k: [{"name": p["name"], "uuid": p["uuid"], "avatar": p["avatar"], "score": (
            p["play_time_str"] if k == "play_time" else (
                f"Nivel {p['total_skill_level']} (Prom: {p['skill_average']})" if k == "auraskills" else (
                    f"{p['distances']['total_km']} km" if k == "distance" else (
                        f"{p['kdr']} K/D" if k == "kdr" else (
                            f"{p['total_mined']:,}" if k == "mined" else (
                                f"{p['total_crafted']:,}" if k == "crafted" else (
                                    f"{p['player_kills']:,}" if k == "player_kills" else f"{p['mob_kills']:,}"
                                )
                            )
                        )
                    )
                )
            )
        )} for p in v] for k, v in leaderboards.items()},
        "players": players
    }

    os.makedirs('dist', exist_ok=True)
    with open('dist/stats_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    with open('stats_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Base de datos generada exitosamente con {len(players)} jugadores.")

if __name__ == '__main__':
    build_database()
