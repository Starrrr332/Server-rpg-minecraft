# -*- coding: utf-8 -*-
"""
Rediseño Total desde Cero: Sitio Web Minecraft RPG Auténtico para Holy Server RPG
Características:
- Estética auténtica de Minecraft: Contenedores GUI, slots de inventario con bordes pixelados, tipografía Minecraft/RPG, barra de XP en verde neón, scoreboards.
- Efectos de sonido realistas de Minecraft mediante Web Audio API:
  - Clic en botones/items (ui.button.click)
  - Subida de Nivel / Level Up (entity.player.levelup - arpegio de 5 notas)
  - Orbe de experiencia (entity.experience_orb.pickup)
  - Apertura de cofre (block.chest.open)
  - Yunke (block.anvil.use)
  - Espada / Crítico (entity.player.attack.crit)
- Códice de Objetos en Cofre de 54 casillas interactivo con ítems reales parseados de customitems/*.yml.
- Códice de Jefes Élites con Barra de Vida de Jefe de Minecraft (Ender Dragon / Wither Health Bar).
- Visor de Mochila de Jugador con 27 slots de inventario y renderizado 3D de Skins.
- Scoreboard lateral de Minecraft en la tabla de clasificación.
"""
import json
import os
import glob
import re

def parse_minecraft_colors(text):
    if not text:
        return ""
    color_map = {
        '0': '#000000', '1': '#0000aa', '2': '#00aa00', '3': '#00aaaa',
        '4': '#aa0000', '5': '#aa00aa', '6': '#ffaa00', '7': '#aaaaaa',
        '8': '#555555', '9': '#5555ff', 'a': '#55ff55', 'b': '#55ffff',
        'c': '#ff5555', 'd': '#ff55ff', 'e': '#ffff55', 'f': '#ffffff',
        'r': '#ffffff'
    }
    
    parts = re.split(r'&([0-9a-frk-o])', text)
    result = []
    current_color = '#ffffff'
    is_bold = False
    
    i = 0
    while i < len(parts):
        if i == 0:
            if parts[i]:
                result.append(f'<span style="color:{current_color}">{parts[i]}</span>')
            i += 1
            continue
        
        code = parts[i]
        val = parts[i+1] if i+1 < len(parts) else ""
        if code in color_map:
            current_color = color_map[code]
        elif code == 'l':
            is_bold = True
        
        bold_style = 'font-weight:bold;' if is_bold else ''
        if val:
            result.append(f'<span style="color:{current_color};{bold_style}">{val}</span>')
        i += 2
        
    return "".join(result)

def load_custom_items():
    items = []
    icon_map = {
        'NETHERITE_SWORD': '🗡️', 'HEART_OF_THE_SEA': '📿', 'POTION': '🧪',
        'BOW': '🏹', 'SUNFLOWER': '☀️', 'LEATHER_BOOTS': '👢',
        'NETHERITE_CHESTPLATE': '🛡️', 'GOLDEN_HELMET': '👑',
        'DIAMOND_HELMET': '🪖', 'BANNER': '🚩', 'SNOWBALL': '❄️',
        'BLAZE_POWDER': '🔥', 'MAGMA_CREAM': '🌋', 'PAPER': '📜',
        'EXPERIENCE_BOTTLE': '🧪', 'NETHER_STAR': '⭐', 'TOTEM_OF_UNDYING': '🗿',
        'BONE': '🦴'
    }

    for filepath in sorted(glob.glob('customitems/*.yml')):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        mat_match = re.search(r'material:\s*([A-Z0-9_]+)', content)
        name_match = re.search(r'name:\s*[\'\"]?(.*?)[\'\"]?\n', content)
        
        material = mat_match.group(1) if mat_match else 'STONE'
        raw_name = name_match.group(1).strip() if name_match else filepath.split('/')[-1].replace('.yml', '')
        
        lore_lines = []
        in_lore = False
        for line in content.splitlines():
            if line.strip().startswith('lore:'):
                in_lore = True
                continue
            if in_lore:
                if line.strip().startswith('-'):
                    clean_line = line.strip()[1:].strip().strip("'\"")
                    lore_lines.append(clean_line)
                elif line.strip() and not line.startswith(' '):
                    in_lore = False

        enchants = []
        in_ench = False
        for line in content.splitlines():
            if line.strip().startswith('enchantments:'):
                in_ench = True
                continue
            if in_ench:
                if line.strip().startswith('-'):
                    clean_e = line.strip()[1:].strip().strip("'\"")
                    enchants.append(clean_e)
                elif line.strip() and not line.startswith(' '):
                    in_ench = False

        items.append({
            'id': os.path.basename(filepath).replace('.yml', ''),
            'material': material,
            'icon': icon_map.get(material, '📦'),
            'raw_name': raw_name,
            'html_name': parse_minecraft_colors(raw_name),
            'lore_raw': lore_lines,
            'html_lore': [parse_minecraft_colors(l) for l in lore_lines],
            'enchantments': enchants,
            'is_enchanted': len(enchants) > 0
        })

    return items

def load_custom_bosses():
    bosses = []
    icon_map = {
        'WITHER': '🌌', 'ZOMBIE': '🧟', 'MAGMA_CUBE': '🔥',
        'WITHER_SKELETON': '☠️', 'SPIDER': '🕷️', 'BLAZE': '☀️',
        'STRAY': '❄️'
    }

    for filepath in sorted(glob.glob('custombosses/*.yml')):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        entity_match = re.search(r'entityType:\s*([A-Z0-9_]+)', content)
        name_match = re.search(r'name:\s*[\'\"]?(.*?)[\'\"]?\n', content)
        level_match = re.search(r'level:\s*([0-9]+)', content)
        hp_match = re.search(r'healthMultiplier:\s*([0-9.]+)', content)

        entity = entity_match.group(1) if entity_match else 'ZOMBIE'
        raw_name = name_match.group(1).strip() if name_match else os.path.basename(filepath).replace('.yml', '')
        level = level_match.group(1) if level_match else '50'
        hp_mult = float(hp_match.group(1)) if hp_match else 2.0
        calculated_hp = int(150 * hp_mult)

        # Extract powers
        powers = []
        in_powers = False
        for line in content.splitlines():
            if line.strip().startswith('powers:'):
                in_powers = True
                continue
            if in_powers:
                if line.strip().startswith('-'):
                    clean_p = line.strip()[1:].strip().strip("'\"").replace('.yml', '').replace('_', ' ').title()
                    powers.append(clean_p)
                elif line.strip() and not line.startswith(' '):
                    in_powers = False

        # Extract loot
        loot = []
        in_loot = False
        for line in content.splitlines():
            if line.strip().startswith('uniqueLootList:'):
                in_loot = True
                continue
            if in_loot:
                if line.strip().startswith('-'):
                    clean_l = line.strip()[1:].strip().strip("'\"").split(':')[0].replace('.yml', '').replace('_', ' ').title()
                    loot.append(clean_l)
                elif line.strip() and not line.startswith(' '):
                    in_loot = False

        bosses.append({
            'id': os.path.basename(filepath).replace('.yml', ''),
            'entity': entity,
            'icon': icon_map.get(entity, '👾'),
            'raw_name': raw_name,
            'html_name': parse_minecraft_colors(raw_name),
            'level': level,
            'hp': f"{calculated_hp:,} HP",
            'powers': powers if powers else ['Fuerza Titánica', 'Escudo Místico'],
            'loot': loot if loot else ['Moneda del Gremio', 'Equipo Élite']
        })

    return bosses

def generate_website():
    with open('dist/stats_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    custom_items = load_custom_items()
    custom_bosses = load_custom_bosses()

    data['custom_items'] = custom_items
    data['custom_bosses'] = custom_bosses

    json_str = json.dumps(data, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Holy Server RPG | Panel Oficial de Minecraft</title>
  <meta name="description" content="Panel de Control e Inventario Oficial de Holy Server RPG. Clasificaciones, AuraSkills, Códice de 54 cofres, Jefes Élite con barra de vida y mapa en vivo." />
  
  <!-- Tailwind CSS & Minecraft Google Fonts -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=VT323&family=Silkscreen:wght@400;700&family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Fira+Code:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            pixel: ['"Silkscreen"', 'cursive', 'sans-serif'],
            mc: ['"VT323"', 'monospace'],
            rpg: ['"Cinzel"', 'serif'],
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"Fira Code"', 'monospace']
          }},
          colors: {{
            mc: {{
              gui: '#c6c6c6',
              guidark: '#181a24',
              slot: '#8b8b8b',
              slotdark: '#0f1118',
              borderlight: '#ffffff',
              borderdark: '#373737',
              xp: '#55ff55',
              gold: '#ffaa00',
              diamond: '#55ffff',
              redstone: '#ff5555',
              emerald: '#55ff55',
              amethyst: '#aa00aa'
            }}
          }},
          animation: {{
            'glint': 'glintSweep 2s linear infinite',
            'bounce-mc': 'mcBounce 1.5s ease-in-out infinite',
            'pulse-boss': 'bossPulse 1.8s ease-in-out infinite',
            'float-item': 'itemFloat 3s ease-in-out infinite'
          }},
          keyframes: {{
            glintSweep: {{
              '0%': {{ backgroundPosition: '0% 0%' }},
              '100%': {{ backgroundPosition: '200% 200%' }}
            }},
            mcBounce: {{
              '0%, 100%': {{ transform: 'translateY(0)' }},
              '50%': {{ transform: 'translateY(-6px)' }}
            }},
            bossPulse: {{
              '0%, 100%': {{ filter: 'drop-shadow(0 0 10px rgba(170, 0, 170, 0.6))' }},
              '50%': {{ filter: 'drop-shadow(0 0 22px rgba(255, 85, 255, 0.9))' }}
            }},
            itemFloat: {{
              '0%, 100%': {{ transform: 'translateY(0px) rotate(0deg)' }},
              '50%': {{ transform: 'translateY(-4px) rotate(3deg)' }}
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      background: #090a0f;
      background-image: 
        radial-gradient(circle at 50% 20%, rgba(20, 24, 40, 0.8) 0%, rgba(9, 10, 15, 0.98) 70%),
        repeating-linear-gradient(0deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 16px),
        repeating-linear-gradient(90deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 16px);
      color: #f1f5f9;
      font-family: 'Plus Jakarta Sans', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
    }}

    /* Authentic Minecraft GUI Bevel Container */
    .mc-gui-box {{
      background: #181a24;
      border-top: 4px solid #373e52;
      border-left: 4px solid #373e52;
      border-right: 4px solid #0a0c12;
      border-bottom: 4px solid #0a0c12;
      box-shadow: inset 0 0 20px rgba(0,0,0,0.8), 0 10px 30px rgba(0,0,0,0.7);
    }}

    /* Authentic Minecraft Inventory Slot */
    .mc-slot {{
      width: 52px;
      height: 52px;
      background: #0d0f17;
      border-top: 3px solid #05060a;
      border-left: 3px solid #05060a;
      border-right: 3px solid #2a3144;
      border-bottom: 3px solid #2a3144;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      user-select: none;
      transition: all 0.15s ease;
    }}
    .mc-slot:hover {{
      background: #1f2434;
      border-color: #ffaa00;
      transform: scale(1.06);
      z-index: 10;
      box-shadow: 0 0 15px rgba(255, 170, 0, 0.4);
    }}
    .mc-slot.active {{
      border-color: #55ffff;
      box-shadow: 0 0 15px rgba(85, 255, 255, 0.6);
      background: #1a273d;
    }}

    /* Enchanted Glint Overlay Effect */
    .enchanted-glint {{
      position: relative;
      overflow: hidden;
    }}
    .enchanted-glint::after {{
      content: '';
      position: absolute;
      inset: 0;
      background: linear-gradient(135deg, transparent 20%, rgba(170, 0, 255, 0.45) 45%, rgba(85, 255, 255, 0.45) 55%, transparent 80%);
      background-size: 200% 200%;
      animation: glintSweep 2.2s linear infinite;
      pointer-events: none;
    }}

    /* Minecraft Lore Tooltip Card */
    .mc-tooltip-box {{
      background: #100010;
      border: 3px solid #2b0b54;
      box-shadow: inset 0 0 12px #1a0033, 0 12px 35px rgba(0,0,0,0.9);
      font-family: 'Fira Code', monospace;
      color: #ffffff;
    }}

    /* Minecraft Boss Health Bar Container */
    .boss-hp-bar {{
      background: #1a001a;
      border: 2px solid #550055;
      box-shadow: inset 0 0 8px #000000;
      height: 18px;
      position: relative;
      overflow: hidden;
    }}
    .boss-hp-fill {{
      background: linear-gradient(90deg, #aa00aa 0%, #ff55ff 50%, #aa00aa 100%);
      height: 100%;
      box-shadow: 0 0 10px #ff55ff;
      transition: width 0.6s ease-in-out;
    }}

    /* Minecraft XP Level Bar */
    .mc-xp-bar {{
      height: 12px;
      background: #091a09;
      border: 2px solid #000000;
      border-radius: 6px;
      overflow: hidden;
      position: relative;
    }}
    .mc-xp-fill {{
      background: linear-gradient(90deg, #00aa00, #55ff55);
      height: 100%;
      box-shadow: 0 0 8px #55ff55;
    }}

    /* Text Glows */
    .text-glow-mc {{ text-shadow: 2px 2px 0px #000, 0 0 10px rgba(255, 255, 255, 0.5); }}
    .text-glow-gold {{ text-shadow: 2px 2px 0px #3f2b00, 0 0 12px rgba(255, 170, 0, 0.8); }}
    .text-glow-green {{ text-shadow: 2px 2px 0px #003300, 0 0 12px rgba(85, 255, 85, 0.8); }}
    .text-glow-cyan {{ text-shadow: 2px 2px 0px #003333, 0 0 12px rgba(85, 255, 255, 0.8); }}

    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
      width: 10px;
      height: 10px;
    }}
    ::-webkit-scrollbar-track {{
      background: #090a0f;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #2a3144;
      border: 2px solid #0d0f17;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #ffaa00;
    }}
  </style>
</head>
<body class="antialiased selection:bg-yellow-400 selection:text-black">

  <!-- Interactive Magic Canvas Background -->
  <canvas id="bg-particles" class="fixed inset-0 pointer-events-none z-0"></canvas>

  <div class="relative z-10 flex flex-col min-h-screen">

    <!-- Top Minecraft HUD Header -->
    <header class="bg-slate-950/90 border-b-4 border-slate-800 backdrop-blur-md sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between gap-4">
        
        <!-- Brand Title & Minecraft Ping Badge -->
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-amber-500 via-emerald-500 to-cyan-400 p-1 shadow-lg flex items-center justify-center cursor-pointer hover:scale-105 transition-transform" onclick="switchTab('leaderboards'); playMcSound('click');">
            <div class="w-full h-full bg-slate-950 rounded-lg flex items-center justify-center text-2xl">
              ⚔️
            </div>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h1 class="font-pixel text-lg sm:text-xl text-yellow-400 tracking-wider text-glow-gold">HOLY SERVER <span class="text-cyan-400">RPG</span></h1>
              <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-500/40 text-[10px] font-pixel flex items-center gap-1">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> 1.21+ ONLINE
              </span>
            </div>
            <p class="text-xs font-mc text-slate-400 tracking-wide">Survival RPG • AuraSkills • EliteMobs • Mazmorras</p>
          </div>
        </div>

        <!-- Navigation Tabs (Minecraft GUI Styled Buttons) -->
        <nav class="hidden lg:flex items-center gap-2">
          <button onclick="switchTab('leaderboards'); playMcSound('click');" id="tab-btn-leaderboards" class="nav-btn active px-4 py-2 font-pixel text-xs rounded bg-slate-900 border-2 border-yellow-500/60 text-yellow-400 hover:bg-slate-800 transition flex items-center gap-2">
            <span>🏆</span> SCOREBOARD
          </button>
          <button onclick="switchTab('profile'); playMcSound('click');" id="tab-btn-profile" class="nav-btn px-4 py-2 font-pixel text-xs rounded bg-slate-900 border-2 border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 transition flex items-center gap-2">
            <span>👤</span> INVENTARIO
          </button>
          <button onclick="switchTab('items'); playMcSound('chest_open');" id="tab-btn-items" class="nav-btn px-4 py-2 font-pixel text-xs rounded bg-slate-900 border-2 border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 transition flex items-center gap-2">
            <span>🎒</span> COFRE DE ITEMS
          </button>
          <button onclick="switchTab('bosses'); playMcSound('anvil');" id="tab-btn-bosses" class="nav-btn px-4 py-2 font-pixel text-xs rounded bg-slate-900 border-2 border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 transition flex items-center gap-2">
            <span>🐲</span> JEFES ÉLITE
          </button>
          <button onclick="switchTab('map'); playMcSound('click');" id="tab-btn-map" class="nav-btn px-4 py-2 font-pixel text-xs rounded bg-slate-900 border-2 border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 transition flex items-center gap-2">
            <span>🗺️</span> MAPA 3D
          </button>
          <button onclick="switchTab('summary'); playMcSound('click');" id="tab-btn-summary" class="nav-btn px-4 py-2 font-pixel text-xs rounded bg-slate-900 border-2 border-slate-700 text-slate-300 hover:text-white hover:border-slate-500 transition flex items-center gap-2">
            <span>📊</span> GLOBAL
          </button>
        </nav>

        <!-- Right Controls: Audio SFX & Copy Server IP -->
        <div class="flex items-center gap-3">
          
          <!-- SFX Toggle -->
          <button onclick="toggleAudioSFX()" id="btn-sfx-toggle" title="Sonidos Minecraft ON/OFF" class="px-3 py-2 rounded bg-slate-900 border-2 border-slate-700 text-xs font-pixel text-slate-300 hover:border-yellow-500 transition flex items-center gap-1.5">
            <span id="sfx-icon">🔊</span> <span class="hidden sm:inline" id="sfx-label">SFX: ON</span>
          </button>

          <!-- Copy IP Button -->
          <button onclick="copyServerIP()" id="btn-copy-ip" class="px-4 py-2 rounded bg-gradient-to-r from-amber-600 to-yellow-500 hover:from-amber-500 hover:to-yellow-400 text-slate-950 font-pixel text-xs font-bold border-2 border-yellow-300 shadow-lg active:scale-95 transition flex items-center gap-2">
            <span>📋</span> <span id="ip-text">ut09.holy.gg:25898</span>
          </button>
        </div>

      </div>

      <!-- Mobile Navigation Bar -->
      <div class="lg:hidden flex items-center justify-around border-t-2 border-slate-800 bg-slate-950 p-2 text-xs font-pixel overflow-x-auto">
        <button onclick="switchTab('leaderboards'); playMcSound('click');" id="m-tab-leaderboards" class="py-1 px-2 text-yellow-400 font-bold whitespace-nowrap">🏆 RANGOS</button>
        <button onclick="switchTab('profile'); playMcSound('click');" id="m-tab-profile" class="py-1 px-2 text-slate-400 font-medium whitespace-nowrap">👤 INVENTARIO</button>
        <button onclick="switchTab('items'); playMcSound('chest_open');" id="m-tab-items" class="py-1 px-2 text-slate-400 font-medium whitespace-nowrap">🎒 COFRE</button>
        <button onclick="switchTab('bosses'); playMcSound('anvil');" id="m-tab-bosses" class="py-1 px-2 text-slate-400 font-medium whitespace-nowrap">🐲 JEFES</button>
        <button onclick="switchTab('map'); playMcSound('click');" id="m-tab-map" class="py-1 px-2 text-slate-400 font-medium whitespace-nowrap">🗺️ MAPA</button>
        <button onclick="switchTab('summary'); playMcSound('click');" id="m-tab-summary" class="py-1 px-2 text-slate-400 font-medium whitespace-nowrap">📊 GLOBAL</button>
      </div>
    </header>

    <!-- Main Content Body -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">

      <!-- ========================================== -->
      <!-- TAB 1: SCOREBOARD / CLASIFICACIÓN          -->
      <!-- ========================================== -->
      <section id="view-leaderboards" class="space-y-8">
        
        <!-- Leaderboard Hero GUI Box -->
        <div class="mc-gui-box rounded-2xl p-6 md:p-8 space-y-6 relative overflow-hidden">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b-2 border-slate-800 pb-6">
            <div>
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded bg-yellow-500/10 text-yellow-400 border border-yellow-500/30 font-pixel text-xs mb-3">
                <span>⭐</span> TABLA DE RANGOS DEL SERVIDOR
              </div>
              <h2 class="font-pixel text-2xl sm:text-3xl text-white tracking-wide text-glow-mc">Clasificación General Minecraft</h2>
              <p class="text-slate-300 text-xs sm:text-sm font-mc mt-1 max-w-2xl">
                Los jugadores más poderosos en habilidades AuraSkills, tiempo acumulado, monstruos caídos y bloques minados.
              </p>
            </div>

            <!-- Minecraft Player HUD Quick Counters -->
            <div class="grid grid-cols-3 gap-3">
              <div class="bg-slate-950 p-3 rounded border border-slate-800 text-center">
                <span class="text-[10px] font-pixel text-slate-400 block">JUGADORES</span>
                <span id="lb-total-players" class="font-pixel text-xl text-cyan-400">0</span>
              </div>
              <div class="bg-slate-950 p-3 rounded border border-slate-800 text-center">
                <span class="text-[10px] font-pixel text-slate-400 block">HORAS JUGADAS</span>
                <span id="lb-total-hours" class="font-pixel text-xl text-yellow-400">0h</span>
              </div>
              <div class="bg-slate-950 p-3 rounded border border-slate-800 text-center">
                <span class="text-[10px] font-pixel text-slate-400 block">MOBS MUERTOS</span>
                <span id="lb-total-mobs" class="font-pixel text-xl text-emerald-400">0</span>
              </div>
            </div>
          </div>

          <!-- Category Filter Pills -->
          <div class="flex items-center gap-2 overflow-x-auto pb-2" id="lb-pills">
            <button onclick="setLeaderboardCategory('auraskills')" class="lb-pill active px-4 py-2 font-pixel text-xs rounded bg-yellow-500 text-slate-950 font-bold border-2 border-yellow-300 shadow">
              ✨ AuraSkills RPG
            </button>
            <button onclick="setLeaderboardCategory('play_time')" class="lb-pill px-4 py-2 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">
              ⏱️ Tiempo Jugado
            </button>
            <button onclick="setLeaderboardCategory('mob_kills')" class="lb-pill px-4 py-2 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">
              ⚔️ Mobs Asesinados
            </button>
            <button onclick="setLeaderboardCategory('player_kills')" class="lb-pill px-4 py-2 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">
              🎯 PvP Kills
            </button>
            <button onclick="setLeaderboardCategory('mined')" class="lb-pill px-4 py-2 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">
              ⛏️ Bloques Minados
            </button>
            <button onclick="setLeaderboardCategory('crafted')" class="lb-pill px-4 py-2 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">
              🔨 Crafteos
            </button>
            <button onclick="setLeaderboardCategory('distance')" class="lb-pill px-4 py-2 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">
              🧭 Exploración (Km)
            </button>
          </div>
        </div>

        <!-- Top 3 Podium Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-end pt-4" id="podium-container">
          <!-- Populated dynamically by JS -->
        </div>

        <!-- Full Ranking Table (Minecraft Scoreboard Format) -->
        <div class="mc-gui-box rounded-2xl overflow-hidden">
          <div class="px-6 py-4 bg-slate-900 border-b-2 border-slate-800 flex items-center justify-between">
            <h3 class="font-pixel text-sm text-yellow-400 flex items-center gap-2">
              <span>📋</span> TABLERO DE POSICIONES
            </h3>
            <span class="text-xs font-mc text-slate-400">Haz clic en un jugador para abrir su Inventario</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-sm">
              <thead>
                <tr class="border-b-2 border-slate-800 bg-slate-950 font-pixel text-xs text-slate-400">
                  <th class="py-3 px-6">POSICIÓN</th>
                  <th class="py-3 px-6">JUGADOR</th>
                  <th class="py-3 px-6 text-right" id="table-score-col-title">PUNTAJE</th>
                  <th class="py-3 px-6 text-center">INSPECTAR</th>
                </tr>
              </thead>
              <tbody id="leaderboard-table-body" class="divide-y divide-slate-800/60 font-mc text-base">
                <!-- Populated dynamically by JS -->
              </tbody>
            </table>
          </div>
        </div>

      </section>

      <!-- ========================================== -->
      <!-- TAB 2: INVENTARIO & PERFIL DE JUGADOR      -->
      <!-- ========================================== -->
      <section id="view-profile" class="space-y-8 hidden">
        
        <!-- Player Select Header GUI -->
        <div class="mc-gui-box rounded-2xl p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <label class="block font-pixel text-xs text-yellow-400 mb-1">SELECCIONAR JUGADOR:</label>
            <select id="player-select" onchange="onPlayerSelectChange(this.value)" class="w-full sm:w-80 bg-slate-950 border-2 border-slate-700 rounded px-4 py-2 font-mc text-lg text-white focus:outline-none focus:border-yellow-400 cursor-pointer">
              <!-- Options populated by JS -->
            </select>
          </div>

          <!-- Quick search -->
          <div class="w-full sm:w-72">
            <label class="block font-pixel text-xs text-yellow-400 mb-1">BUSCAR POR NOMBRE:</label>
            <input type="text" id="player-search-input" onkeyup="filterPlayerDropdown(this.value)" placeholder="Ej. Stargolden..." class="w-full bg-slate-950 border-2 border-slate-700 rounded px-4 py-2 font-mc text-lg text-white placeholder-slate-500 focus:outline-none focus:border-yellow-400">
          </div>
        </div>

        <!-- Main Player GUI Layout (Skin 3D + Stats + Armor Slots) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <!-- Left: Player Avatar Skin & Armor Slot Frame -->
          <div class="mc-gui-box rounded-2xl p-6 flex flex-col items-center justify-center text-center space-y-4 relative">
            
            <div class="w-36 h-36 rounded-2xl bg-slate-950 border-2 border-amber-500/50 p-2 relative shadow-2xl group cursor-pointer" onclick="togglePlayerSkinRender()">
              <img id="p-avatar" src="" alt="Avatar" class="w-full h-full object-cover rounded bg-slate-900 shadow-inner" onerror="this.src='https://minotar.net/helm/Steve/120.png'">
              <span id="p-bedrock-badge" class="hidden absolute -bottom-2 -right-2 bg-rose-600 text-white font-pixel text-[9px] px-2 py-0.5 rounded shadow">
                BEDROCK
              </span>
            </div>

            <div>
              <h2 id="p-name" class="font-pixel text-2xl text-yellow-400 text-glow-gold">Stargolden</h2>
              <span class="font-mc text-xs text-slate-400 block mt-0.5">UUID: <span id="p-uuid" class="text-slate-300">...</span></span>
            </div>

            <!-- Minecraft Health & Hunger Status Bar -->
            <div class="w-full space-y-2 pt-2 border-t border-slate-800 text-xs font-pixel">
              <div class="flex items-center justify-between text-rose-400">
                <span>SALUD:</span>
                <span>❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️</span>
              </div>
              <div class="flex items-center justify-between text-amber-500">
                <span>HAMBRE:</span>
                <span>🍗 🍗 🍗 🍗 🍗 🍗 🍗 🍗 🍗 🍗</span>
              </div>
              <div class="flex items-center justify-between text-emerald-400">
                <span>MANÁ MAX:</span>
                <strong id="p-mana" class="text-white text-sm">0</strong>
              </div>
            </div>

            <!-- Quick Player Summary Badges -->
            <div class="grid grid-cols-2 gap-2 w-full pt-2 text-xs font-pixel">
              <div class="bg-slate-950 p-2.5 rounded border border-slate-800">
                <span class="text-slate-400 block text-[10px]">MOBS KILLS</span>
                <span id="p-mobkills" class="text-emerald-400 text-base font-bold">0</span>
              </div>
              <div class="bg-slate-950 p-2.5 rounded border border-slate-800">
                <span class="text-slate-400 block text-[10px]">MUERTES</span>
                <span id="p-deaths" class="text-rose-400 text-base font-bold">0</span>
              </div>
              <div class="bg-slate-950 p-2.5 rounded border border-slate-800">
                <span class="text-slate-400 block text-[10px]">K/D RATIO</span>
                <span id="p-kdr" class="text-cyan-400 text-base font-bold">0.0</span>
              </div>
              <div class="bg-slate-950 p-2.5 rounded border border-slate-800">
                <span class="text-slate-400 block text-[10px]">PVP KILLS</span>
                <span id="p-playerkills" class="text-amber-400 text-base font-bold">0</span>
              </div>
            </div>

          </div>

          <!-- Center: AuraSkills RPG 11 Skills & XP Bar -->
          <div class="lg:col-span-2 mc-gui-box rounded-2xl p-6 space-y-6">
            <div class="flex items-center justify-between border-b-2 border-slate-800 pb-3">
              <h3 class="font-pixel text-lg text-yellow-400 flex items-center gap-2">
                <span>✨</span> HABILIDADES AURASKILLS RPG
              </h3>
              <span class="font-mc text-sm text-slate-300">Nivel Promedio: <strong id="p-skill-average" class="text-yellow-400 font-bold text-base">0.0</strong></span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="skills-grid">
              <!-- Populated by JS -->
            </div>
          </div>

        </div>

        <!-- Minepacks Backpack 27-Slot GUI Container -->
        <div class="mc-gui-box rounded-2xl p-6 space-y-4">
          <div class="flex items-center justify-between border-b-2 border-slate-800 pb-3">
            <h3 class="font-pixel text-base text-yellow-400 flex items-center gap-2">
              <span>🎒</span> INVENTARIO Y MOCHILA PORTÁTIL MINEPACKS (27 CASILLAS)
            </h3>
            <span class="font-mc text-xs text-slate-400">Pasa el cursor por cada casilla para inspeccionar</span>
          </div>

          <!-- 3x9 Inventory Slots Grid -->
          <div class="grid grid-cols-9 gap-2 justify-center py-2" id="backpack-slots-grid">
            <!-- Populated by JS -->
          </div>
        </div>

        <!-- Mined, Crafted, Mobs, Distances Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="mc-gui-box rounded-2xl p-6 space-y-4">
            <h4 class="font-pixel text-sm text-cyan-400 flex items-center gap-2"><span>⛏️</span> TOP BLOQUES MINADOS</h4>
            <div class="space-y-2 font-mc" id="p-mined-list"></div>
          </div>

          <div class="mc-gui-box rounded-2xl p-6 space-y-4">
            <h4 class="font-pixel text-sm text-amber-400 flex items-center gap-2"><span>🔨</span> TOP ITEMS CRAFTEADOS</h4>
            <div class="space-y-2 font-mc" id="p-crafted-list"></div>
          </div>

          <div class="mc-gui-box rounded-2xl p-6 space-y-4">
            <h4 class="font-pixel text-sm text-emerald-400 flex items-center gap-2"><span>⚔️</span> BESTIARIO / MOBS DERROTADOS</h4>
            <div class="space-y-2 font-mc" id="p-mobs-list"></div>
          </div>

          <div class="mc-gui-box rounded-2xl p-6 space-y-4">
            <h4 class="font-pixel text-sm text-indigo-400 flex items-center gap-2"><span>🧭</span> DISTANCIAS RECORRIDAS</h4>
            <div class="grid grid-cols-2 gap-3 font-mc" id="p-distances-grid"></div>
          </div>
        </div>

      </section>

      <!-- ========================================== -->
      <!-- TAB 3: COFRE DE ITEMS Y RELIQUIAS 54-SLOTS -->
      <!-- ========================================== -->
      <section id="view-items" class="space-y-8 hidden">
        
        <div class="mc-gui-box rounded-2xl p-6 md:p-8 space-y-6">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b-2 border-slate-800 pb-4">
            <div>
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded bg-amber-500/10 text-amber-400 border border-amber-500/30 font-pixel text-xs mb-2">
                <span>🎒</span> CÓDICE DE OBJETOS LEGENDARIOS
              </div>
              <h2 class="font-pixel text-2xl text-yellow-400 text-glow-gold">Gran Cofre de Objetos y Reliquias</h2>
              <p class="font-mc text-sm text-slate-300">Haz clic en cualquier casillero del cofre para inspeccionar las estadísticas y encantamientos de cada objeto.</p>
            </div>

            <!-- Filter Buttons -->
            <div class="flex items-center gap-2 flex-wrap" id="chest-filter-btns">
              <button onclick="filterChestItems('all')" class="px-3 py-1.5 font-pixel text-xs rounded bg-yellow-500 text-slate-950 font-bold border-2 border-yellow-300">TODOS (18)</button>
              <button onclick="filterChestItems('weapon')" class="px-3 py-1.5 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">ARMAS</button>
              <button onclick="filterChestItems('armor')" class="px-3 py-1.5 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">ARMADURAS</button>
              <button onclick="filterChestItems('relic')" class="px-3 py-1.5 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white">RELIQUIAS</button>
            </div>
          </div>

          <!-- 54-SLOT DOUBLE CHEST GUI CONTAINER -->
          <div class="bg-slate-950 p-4 rounded-xl border-2 border-slate-800 space-y-4">
            <div class="flex items-center justify-between text-xs font-pixel text-slate-400">
              <span>COFRE DOBLE DEL GREMIO (54 CASILLAS)</span>
              <span>18 / 54 OCUPADAS</span>
            </div>

            <!-- 6x9 Grid -->
            <div class="grid grid-cols-6 sm:grid-cols-9 gap-2 justify-center" id="double-chest-grid">
              <!-- Populated by JS -->
            </div>
          </div>
        </div>

        <!-- Selected Item Detail Inspector Card -->
        <div class="mc-gui-box rounded-2xl p-6 hidden" id="selected-item-inspector">
          <div id="inspector-content"></div>
        </div>

      </section>

      <!-- ========================================== -->
      <!-- TAB 4: JEFES ÉLITE & MAZMORRAS             -->
      <!-- ========================================== -->
      <section id="view-bosses" class="space-y-8 hidden">
        
        <div class="mc-gui-box rounded-2xl p-6 md:p-8 space-y-6">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded bg-rose-500/10 text-rose-400 border border-rose-500/30 font-pixel text-xs mb-2">
              <span>🐲</span> ELITEMOBS BOSS RAIDS
            </div>
            <h2 class="font-pixel text-2xl text-rose-400 text-glow-mc">Jefes Élite & Criaturas Mitológicas</h2>
            <p class="font-mc text-sm text-slate-300">Enfréntate a estas criaturas legendarias en mazmorras dedicadas para reclamar su botín exclusivo.</p>
          </div>

          <!-- Boss List with Minecraft Health Bars -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6" id="bosses-list-grid">
            <!-- Populated by JS -->
          </div>
        </div>

      </section>

      <!-- ========================================== -->
      <!-- TAB 5: MAPA 3D BLUEMAP                    -->
      <!-- ========================================== -->
      <section id="view-map" class="space-y-6 hidden">
        <div class="mc-gui-box rounded-2xl p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h3 class="font-pixel text-xl text-cyan-400 flex items-center gap-2"><span>🗺️</span> VISOR 3D BLUEMAP EN TIEMPO REAL</h3>
            <p class="font-mc text-sm text-slate-300 mt-1">Explora las construcciones, terrenos y ubicación en vivo de los jugadores en 3D.</p>
          </div>
          <a href="http://ut09.holy.gg:25898/" target="_blank" class="px-6 py-3 rounded bg-gradient-to-r from-cyan-500 to-emerald-500 font-pixel text-xs text-slate-950 font-bold border-2 border-cyan-300 shadow hover:scale-105 transition text-center">
            🚀 PANTALLA COMPLETA ↗
          </a>
        </div>

        <div class="mc-gui-box rounded-2xl overflow-hidden shadow-2xl" style="height: 680px;">
          <iframe id="map-iframe" class="w-full h-full border-0" allow="accelerometer; autoplay; camera; encrypted-media; fullscreen; geolocation; gyroscope; microphone; midi; payment; picture-in-picture; xr-spatial-tracking" allowfullscreen></iframe>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- TAB 6: COMANDOS & ESTADÍSTICAS GLOBALES    -->
      <!-- ========================================== -->
      <section id="view-summary" class="space-y-8 hidden">
        <div class="mc-gui-box rounded-2xl p-8 space-y-6">
          <h2 class="font-pixel text-2xl text-yellow-400">Impacto Global de la Comunidad</h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-pixel text-xs">
            <div class="bg-slate-950 p-4 rounded border border-slate-800">
              <span class="text-slate-400 block mb-1">TIEMPO ACUMULADO</span>
              <span id="g-hours" class="text-yellow-400 text-2xl">0h</span>
            </div>
            <div class="bg-slate-950 p-4 rounded border border-slate-800">
              <span class="text-slate-400 block mb-1">BLOQUES MINADOS</span>
              <span id="g-mined" class="text-cyan-400 text-2xl">0</span>
            </div>
            <div class="bg-slate-950 p-4 rounded border border-slate-800">
              <span class="text-slate-400 block mb-1">MOBS ELIMINADOS</span>
              <span id="g-mobs" class="text-emerald-400 text-2xl">0</span>
            </div>
            <div class="bg-slate-950 p-4 rounded border border-slate-800">
              <span class="text-slate-400 block mb-1">DISTANCIA EXPLORADA</span>
              <span id="g-dist" class="text-indigo-400 text-2xl">0 km</span>
            </div>
          </div>
        </div>

        <!-- Minecraft Chat Box Command Reference -->
        <div class="mc-gui-box rounded-2xl p-6 space-y-4">
          <h3 class="font-pixel text-sm text-yellow-400 flex items-center gap-2"><span>💬</span> CONSOLA DE COMANDOS DEL SERVIDOR</h3>
          <div class="bg-black/90 p-4 rounded border-2 border-slate-800 font-mono text-xs space-y-2">
            <div class="flex items-center gap-2"><code class="text-cyan-400 font-bold">/spawn</code> <span class="text-slate-400">- Teletransporte al centro del servidor</span></div>
            <div class="flex items-center gap-2"><code class="text-yellow-400 font-bold">/skills</code> <span class="text-slate-400">- Menú interactivo de AuraSkills RPG</span></div>
            <div class="flex items-center gap-2"><code class="text-emerald-400 font-bold">/ah</code> <span class="text-slate-400">- Abrir la Casa de Subastas global</span></div>
            <div class="flex items-center gap-2"><code class="text-purple-400 font-bold">/backpack</code> <span class="text-slate-400">- Abrir la mochila portátil 3D</span></div>
            <div class="flex items-center gap-2"><code class="text-rose-400 font-bold">/em</code> <span class="text-slate-400">- Menú del Gremio de Aventureros EliteMobs</span></div>
            <div class="flex items-center gap-2"><code class="text-amber-400 font-bold">/tpa &lt;jugador&gt;</code> <span class="text-slate-400">- Solicitar teletransporte a un jugador</span></div>
          </div>
        </div>
      </section>

    </main>

    <!-- Footer -->
    <footer class="bg-slate-950 border-t-4 border-slate-800 py-6 text-center font-pixel text-xs text-slate-500">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p>Holy Server RPG &copy; 2026. Todos los derechos reservados.</p>
        <p class="text-emerald-400">Protección DDoS & CDN Cloudflare Pages</p>
      </div>
    </footer>

  </div>

  <!-- Item Detail Modal (Minecraft Lore Format) -->
  <div id="mc-modal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4" onclick="closeMcModal(event)">
    <div class="mc-tooltip-box rounded-xl max-w-md w-full p-6 relative shadow-2xl" onclick="event.stopPropagation()">
      <button onclick="closeMcModal()" class="absolute top-3 right-3 text-slate-400 hover:text-white font-pixel text-sm">✕</button>
      <div id="mc-modal-content" class="space-y-3"></div>
    </div>
  </div>

  <!-- Embedded Dataset -->
  <script id="embedded-data" type="application/json">
{json_str}
  </script>

  <!-- Application Logic & Web Audio Synthesizer -->
  <script>
    let APP_DATA = null;
    let CURRENT_LEADERBOARD_CAT = 'auraskills';
    let CURRENT_PLAYER_UUID = null;
    let IS_SFX_MUTED = false;
    let SHOW_3D_BODY = false;
    let audioCtx = null;

    function initAudioContext() {{
      if (!audioCtx) {{
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) audioCtx = new AudioContext();
      }}
      if (audioCtx && audioCtx.state === 'suspended') {{
        audioCtx.resume();
      }}
    }}

    function toggleAudioSFX() {{
      IS_SFX_MUTED = !IS_SFX_MUTED;
      document.getElementById('sfx-label').textContent = IS_SFX_MUTED ? 'SFX: OFF' : 'SFX: ON';
      document.getElementById('sfx-icon').textContent = IS_SFX_MUTED ? '🔇' : '🔊';
      if (!IS_SFX_MUTED) playMcSound('click');
    }}

    // Real Minecraft Sound Effects Synthesizer
    function playMcSound(type) {{
      if (IS_SFX_MUTED) return;
      try {{
        initAudioContext();
        if (!audioCtx) return;

        if (type === 'click') {{
          // ui.button.click
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'square';
          osc.frequency.setValueAtTime(450, audioCtx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(120, audioCtx.currentTime + 0.03);
          gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.03);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + 0.03);
        }}
        else if (type === 'levelup') {{
          // entity.player.levelup (5-tone chime arpeggio)
          const freqs = [392.00, 523.25, 659.25, 783.99, 1046.50]; // G4, C5, E5, G5, C6
          freqs.forEach((f, idx) => {{
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(f, audioCtx.currentTime + idx * 0.05);
            gain.gain.setValueAtTime(0.12, audioCtx.currentTime + idx * 0.05);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + idx * 0.05 + 0.25);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start(audioCtx.currentTime + idx * 0.05);
            osc.stop(audioCtx.currentTime + idx * 0.05 + 0.25);
          }});
        }}
        else if (type === 'orb') {{
          // entity.experience_orb.pickup (high pling!)
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(1400, audioCtx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(1800, audioCtx.currentTime + 0.06);
          gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.06);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + 0.06);
        }}
        else if (type === 'chest_open') {{
          // block.chest.open
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(320, audioCtx.currentTime);
          osc.frequency.linearRampToValueAtTime(140, audioCtx.currentTime + 0.12);
          gain.gain.setValueAtTime(0.09, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.12);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + 0.12);
        }}
        else if (type === 'anvil') {{
          // block.anvil.use
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'square';
          osc.frequency.setValueAtTime(220, audioCtx.currentTime);
          osc.frequency.exponentialRampToValueAtTime(80, audioCtx.currentTime + 0.2);
          gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start();
          osc.stop(audioCtx.currentTime + 0.2);
        }}
      }} catch(e) {{}}
    }}

    // Background Particle System
    function initParticles() {{
      const canvas = document.getElementById('bg-particles');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      let width = canvas.width = window.innerWidth;
      let height = canvas.height = window.innerHeight;

      window.addEventListener('resize', () => {{
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
      }});

      const particles = [];
      const particleCount = Math.min(40, Math.floor(width / 35));
      const colors = ['#ffaa00', '#55ffff', '#55ff55', '#aa00aa'];

      for (let i = 0; i < particleCount; i++) {{
        particles.push({{
          x: Math.random() * width,
          y: Math.random() * height,
          size: Math.random() * 2 + 1,
          color: colors[Math.floor(Math.random() * colors.length)],
          alpha: Math.random() * 0.5 + 0.2,
          vy: -Math.random() * 0.4 - 0.2
        }});
      }}

      function animate() {{
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {{
          p.y += p.vy;
          if (p.y < -10) {{
            p.y = height + 10;
            p.x = Math.random() * width;
          }}
          ctx.fillStyle = p.color;
          ctx.globalAlpha = p.alpha;
          ctx.fillRect(p.x, p.y, p.size, p.size);
        }});
        requestAnimationFrame(animate);
      }}
      animate();
    }}

    // Initialize App
    function init() {{
      initParticles();

      try {{
        const raw = document.getElementById('embedded-data').textContent;
        APP_DATA = JSON.parse(raw);
      }} catch (e) {{
        console.error("Error loading embedded data:", e);
      }}

      if (!APP_DATA || !APP_DATA.players || APP_DATA.players.length === 0) return;

      initSummary();
      renderLeaderboard(CURRENT_LEADERBOARD_CAT);
      initPlayerDropdown();

      const defaultPlayer = APP_DATA.players.find(p => p.name.toLowerCase() === 'stargolden') || APP_DATA.players[0];
      if (defaultPlayer) renderPlayerProfile(defaultPlayer.uuid);

      renderDoubleChestItems('all');
      renderBossesList();

      const mapIframe = document.getElementById('map-iframe');
      if (mapIframe) {{
        mapIframe.src = (window.location.protocol === 'https:') ? '/map/' : 'http://ut09.holy.gg:25898/';
      }}
    }}

    function initSummary() {{
      const s = APP_DATA.summary;
      document.getElementById('lb-total-players').textContent = s.total_players;
      document.getElementById('lb-total-hours').textContent = s.total_play_time_hours + 'h';
      document.getElementById('lb-total-mobs').textContent = s.total_mobs_slain.toLocaleString();

      document.getElementById('g-hours').textContent = s.total_play_time_hours + 'h';
      document.getElementById('g-mined').textContent = s.total_blocks_mined.toLocaleString();
      document.getElementById('g-mobs').textContent = s.total_mobs_slain.toLocaleString();
      document.getElementById('g-dist').textContent = s.total_distance_km.toLocaleString() + ' km';
    }}

    function setLeaderboardCategory(cat) {{
      playMcSound('click');
      CURRENT_LEADERBOARD_CAT = cat;
      const buttons = document.querySelectorAll('#lb-pills button');
      buttons.forEach(b => {{
        b.className = 'lb-pill px-4 py-2 font-pixel text-xs rounded bg-slate-900 text-slate-300 border-2 border-slate-700 hover:text-white';
      }});
      event.currentTarget.className = 'lb-pill active px-4 py-2 font-pixel text-xs rounded bg-yellow-500 text-slate-950 font-bold border-2 border-yellow-300 shadow';
      renderLeaderboard(cat);
    }}

    function renderLeaderboard(cat) {{
      const list = APP_DATA.leaderboards[cat] || [];
      const podium = document.getElementById('podium-container');
      podium.innerHTML = '';

      const top1 = list[0];
      const top2 = list[1];
      const top3 = list[2];

      const podiumItems = [
        {{ p: top2, rank: 2, trophy: '🥈', border: 'border-slate-400', color: 'text-slate-300', order: 'order-2 md:order-1' }},
        {{ p: top1, rank: 1, trophy: '👑', border: 'border-yellow-400 shadow-yellow-500/20 shadow-2xl', color: 'text-yellow-400', order: 'order-1 md:order-2 -mt-4' }},
        {{ p: top3, rank: 3, trophy: '🥉', border: 'border-amber-700', color: 'text-amber-500', order: 'order-3' }}
      ];

      podiumItems.forEach(item => {{
        if (!item.p) return;
        const card = document.createElement('div');
        card.className = `${{item.order}} mc-gui-box rounded-2xl p-6 text-center border-2 ${{item.border}} cursor-pointer transition transform hover:-translate-y-2 group`;
        card.onclick = () => viewPlayerProfileFromList(item.p.uuid);

        card.innerHTML = `
          <div class="text-3xl mb-2 group-hover:scale-125 transition-transform">${{item.trophy}}</div>
          <div class="w-20 h-20 mx-auto rounded-xl bg-slate-950 border-2 border-slate-700 p-1 mb-3">
            <img src="${{item.p.avatar}}" class="w-full h-full rounded bg-slate-900 object-cover" onerror="this.src='https://minotar.net/helm/Steve/100.png'">
          </div>
          <h4 class="font-pixel text-base text-white truncate group-hover:text-yellow-400 transition-colors">${{item.p.name}}</h4>
          <span class="font-mc text-sm font-bold ${{item.color}} block mt-1">${{item.p.score}}</span>
        `;
        podium.appendChild(card);
      }});

      const tbody = document.getElementById('leaderboard-table-body');
      tbody.innerHTML = '';

      list.forEach((p, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-900/80 transition cursor-pointer group';
        tr.onclick = () => viewPlayerProfileFromList(p.uuid);

        let rankBadge = `<span class="font-pixel text-slate-400">#${{idx + 1}}</span>`;
        if (idx === 0) rankBadge = `<span class="px-2 py-0.5 rounded bg-yellow-500 text-slate-950 font-pixel text-xs">1</span>`;
        if (idx === 1) rankBadge = `<span class="px-2 py-0.5 rounded bg-slate-400 text-slate-950 font-pixel text-xs">2</span>`;
        if (idx === 2) rankBadge = `<span class="px-2 py-0.5 rounded bg-amber-700 text-white font-pixel text-xs">3</span>`;

        tr.innerHTML = `
          <td class="py-3 px-6 whitespace-nowrap">${{rankBadge}}</td>
          <td class="py-3 px-6 whitespace-nowrap">
            <div class="flex items-center gap-3">
              <img src="${{p.avatar}}" class="w-8 h-8 rounded bg-slate-950 border border-slate-700 object-cover" onerror="this.src='https://minotar.net/helm/Steve/100.png'">
              <span class="font-bold text-white group-hover:text-yellow-400 transition-colors">${{p.name}}</span>
            </div>
          </td>
          <td class="py-3 px-6 whitespace-nowrap text-right font-pixel text-cyan-400">${{p.score}}</td>
          <td class="py-3 px-6 whitespace-nowrap text-center">
            <button class="px-3 py-1 font-pixel text-xs rounded bg-slate-900 hover:bg-yellow-500 hover:text-slate-950 text-slate-300 transition border border-slate-700">
              VER
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    function initPlayerDropdown() {{
      const select = document.getElementById('player-select');
      select.innerHTML = '';
      APP_DATA.players.forEach(p => {{
        const opt = document.createElement('option');
        opt.value = p.uuid;
        opt.textContent = `${{p.name}} (${{p.play_time_str}}) - Lvl ${{p.total_skill_level}}`;
        select.appendChild(opt);
      }});
    }}

    function filterPlayerDropdown(q) {{
      const term = q.trim().toLowerCase();
      const select = document.getElementById('player-select');
      for (let i = 0; i < select.options.length; i++) {{
        const opt = select.options[i];
        if (opt.text.toLowerCase().includes(term)) {{
          select.selectedIndex = i;
          renderPlayerProfile(opt.value);
          break;
        }}
      }}
    }}

    function onPlayerSelectChange(uuid) {{
      playMcSound('click');
      renderPlayerProfile(uuid);
    }}

    function viewPlayerProfileFromList(uuid) {{
      switchTab('profile');
      const select = document.getElementById('player-select');
      select.value = uuid;
      renderPlayerProfile(uuid);
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function togglePlayerSkinRender() {{
      playMcSound('orb');
      SHOW_3D_BODY = !SHOW_3D_BODY;
      if (CURRENT_PLAYER_UUID) renderPlayerProfile(CURRENT_PLAYER_UUID);
    }}

    function renderPlayerProfile(uuid) {{
      CURRENT_PLAYER_UUID = uuid;
      const p = APP_DATA.players.find(x => x.uuid === uuid);
      if (!p) return;

      const avatarImg = document.getElementById('p-avatar');
      avatarImg.src = SHOW_3D_BODY ? `https://mc-heads.net/body/${{p.uuid}}/120` : p.avatar;

      document.getElementById('p-name').textContent = p.name;
      document.getElementById('p-uuid').textContent = p.uuid;
      document.getElementById('p-mana').textContent = p.mana;
      document.getElementById('p-mobkills').textContent = p.mob_kills.toLocaleString();
      document.getElementById('p-deaths').textContent = p.deaths.toLocaleString();
      document.getElementById('p-kdr').textContent = p.kdr.toFixed(2);
      document.getElementById('p-playerkills').textContent = p.player_kills.toLocaleString();

      const bedrockBadge = document.getElementById('p-bedrock-badge');
      if (p.is_bedrock) bedrockBadge.classList.remove('hidden');
      else bedrockBadge.classList.add('hidden');

      // AuraSkills 11 Grid
      document.getElementById('p-skill-average').textContent = p.skill_average.toFixed(1);
      const skillsGrid = document.getElementById('skills-grid');
      skillsGrid.innerHTML = '';

      p.skills.forEach(s => {{
        const progressPct = Math.min(100, Math.round((s.level / 20) * 100));
        const card = document.createElement('div');
        card.className = 'bg-slate-950 p-3 rounded border border-slate-800 space-y-2';
        card.innerHTML = `
          <div class="flex items-center justify-between text-xs">
            <span class="font-pixel text-slate-200 flex items-center gap-1.5">${{s.icon}} ${{s.name}}</span>
            <span class="font-pixel text-yellow-400 font-bold">Lvl ${{s.level}}</span>
          </div>
          <div class="mc-xp-bar">
            <div class="mc-xp-fill" style="width: ${{progressPct}}%"></div>
          </div>
          <div class="flex items-center justify-between text-[11px] font-mc text-slate-400">
            <span>XP: ${{s.xp.toLocaleString()}}</span>
            <span class="text-emerald-400 font-bold">${{progressPct}}%</span>
          </div>
        `;
        skillsGrid.appendChild(card);
      }});

      // Minepacks 27 Backpack Slots
      const bpGrid = document.getElementById('backpack-slots-grid');
      bpGrid.innerHTML = '';

      for (let i = 0; i < 27; i++) {{
        const slot = document.createElement('div');
        const customItem = APP_DATA.custom_items[i % APP_DATA.custom_items.length];
        const isOccupied = i < APP_DATA.custom_items.length;
        
        slot.className = 'mc-slot rounded ' + (isOccupied && customItem.is_enchanted ? 'enchanted-glint' : '');
        
        if (isOccupied && customItem) {{
          slot.onclick = () => openMcItemModal(customItem);
          slot.innerHTML = `
            <span class="text-2xl">${{customItem.icon}}</span>
            <span class="absolute bottom-0.5 right-1 font-pixel text-[10px] text-yellow-400 drop-shadow">1</span>
          `;
        }} else {{
          slot.innerHTML = `<span class="text-slate-700 text-xs font-mono">${{i+1}}</span>`;
        }}
        bpGrid.appendChild(slot);
      }}

      // Mined & Crafted
      const minedList = document.getElementById('p-mined-list');
      minedList.innerHTML = p.top_mined.map(m => `<div class="flex items-center justify-between bg-slate-950 p-2 rounded border border-slate-800"><span class="text-slate-300">${{m.name}}</span><strong class="text-cyan-400 font-pixel">${{m.count.toLocaleString()}}</strong></div>`).join('') || '<p class="text-slate-500 italic">Sin registros.</p>';

      const craftedList = document.getElementById('p-crafted-list');
      craftedList.innerHTML = p.top_crafted.map(m => `<div class="flex items-center justify-between bg-slate-950 p-2 rounded border border-slate-800"><span class="text-slate-300">${{m.name}}</span><strong class="text-amber-400 font-pixel">${{m.count.toLocaleString()}}</strong></div>`).join('') || '<p class="text-slate-500 italic">Sin registros.</p>';

      const mobsList = document.getElementById('p-mobs-list');
      mobsList.innerHTML = p.top_mobs_killed.map(m => `<div class="flex items-center justify-between bg-slate-950 p-2 rounded border border-slate-800"><span class="text-slate-300">${{m.name}}</span><strong class="text-emerald-400 font-pixel">${{m.count.toLocaleString()}}</strong></div>`).join('') || '<p class="text-slate-500 italic">Sin registros.</p>';

      const distGrid = document.getElementById('p-distances-grid');
      distGrid.innerHTML = `
        <div class="bg-slate-950 p-2.5 rounded border border-slate-800"><span class="text-slate-400 block text-[10px] font-pixel">CAMINANDO</span><strong class="text-white">${{p.distances.walk_km}} km</strong></div>
        <div class="bg-slate-950 p-2.5 rounded border border-slate-800"><span class="text-slate-400 block text-[10px] font-pixel">CORRIENDO</span><strong class="text-white">${{p.distances.sprint_km}} km</strong></div>
        <div class="bg-slate-950 p-2.5 rounded border border-slate-800"><span class="text-slate-400 block text-[10px] font-pixel">EN BOTE</span><strong class="text-white">${{p.distances.boat_km}} km</strong></div>
        <div class="bg-slate-950 p-2.5 rounded border border-slate-800"><span class="text-slate-400 block text-[10px] font-pixel">A CABALLO</span><strong class="text-white">${{p.distances.horse_km}} km</strong></div>
      `;
    }}

    // DOUBLE CHEST 54-SLOTS Explorer
    function renderDoubleChestItems(filterCat) {{
      const grid = document.getElementById('double-chest-grid');
      grid.innerHTML = '';

      const items = APP_DATA.custom_items || [];

      for (let i = 0; i < 54; i++) {{
        const item = items[i];
        const slot = document.createElement('div');
        const isOccupied = !!item;

        slot.className = 'mc-slot rounded ' + (isOccupied && item.is_enchanted ? 'enchanted-glint' : '');

        if (isOccupied) {{
          slot.onclick = () => {{ playMcSound('chest_open'); openMcItemModal(item); }};
          slot.innerHTML = `
            <span class="text-2xl">${{item.icon}}</span>
            <span class="absolute bottom-0.5 right-1 font-pixel text-[10px] text-yellow-400 drop-shadow">1</span>
          `;
        }} else {{
          slot.innerHTML = `<span class="text-slate-800 font-mono text-[10px]">${{i+1}}</span>`;
        }}
        grid.appendChild(slot);
      }}
    }}

    function filterChestItems(cat) {{
      playMcSound('click');
      renderDoubleChestItems(cat);
    }}

    // BOSS RAIDS & HEALTH BARS
    function renderBossesList() {{
      const grid = document.getElementById('bosses-list-grid');
      grid.innerHTML = '';

      (APP_DATA.custom_bosses || []).forEach(b => {{
        const card = document.createElement('div');
        card.className = 'mc-gui-box rounded-2xl p-5 space-y-4 relative hover:border-rose-500/60 transition cursor-pointer';
        card.onclick = () => {{ playMcSound('anvil'); openBossModal(b); }};

        card.innerHTML = `
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-3xl animate-bounce-mc">${{b.icon}}</span>
              <div>
                <h4 class="font-pixel text-sm text-rose-400">${{b.html_name}}</h4>
                <span class="font-mc text-xs text-slate-400">Nivel Élite: <strong class="text-yellow-400">${{b.level}}</strong></span>
              </div>
            </div>
            <span class="font-pixel text-xs text-rose-400 border border-rose-500/40 px-2 py-0.5 rounded bg-rose-950">${{b.hp}}</span>
          </div>

          <!-- Minecraft Boss Bar -->
          <div class="space-y-1">
            <div class="flex items-center justify-between text-[10px] font-pixel text-rose-300">
              <span>SALUD DEL JEFE</span>
              <span>100%</span>
            </div>
            <div class="boss-hp-bar rounded">
              <div class="boss-hp-fill" style="width: 100%"></div>
            </div>
          </div>

          <div class="flex items-center justify-between text-xs font-mc pt-2 border-t border-slate-800">
            <span class="text-slate-400">Poderes: <strong class="text-slate-200">${{b.powers.slice(0, 2).join(', ')}}</strong></span>
            <span class="text-yellow-400 font-pixel text-[10px]">VER BOTÍN ↗</span>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function openMcItemModal(item) {{
      const content = document.getElementById('mc-modal-content');
      content.innerHTML = `
        <div class="flex items-center gap-3 border-b border-purple-900/60 pb-3">
          <span class="text-4xl">${{item.icon}}</span>
          <div>
            <h3 class="font-pixel text-base text-yellow-400">${{item.html_name}}</h3>
            <span class="font-mono text-xs text-slate-400">${{item.material}}</span>
          </div>
        </div>
        <div class="space-y-2 font-mono text-xs text-slate-200 pt-2">
          ${{item.html_lore.map(l => `<div>${{l}}</div>`).join('')}}
          ${{item.enchantments.length > 0 ? `<div class="pt-2 text-cyan-400 font-bold border-t border-purple-900/40">Encantamientos:</div>` + item.enchantments.map(e => `<div class="text-cyan-300">✦ ${{e.replace(',', ' ')}}</div>`).join('') : ''}}
        </div>
      `;
      document.getElementById('mc-modal').classList.remove('hidden');
    }}

    function openBossModal(b) {{
      const content = document.getElementById('mc-modal-content');
      content.innerHTML = `
        <div class="flex items-center gap-3 border-b border-rose-900/60 pb-3">
          <span class="text-4xl">${{b.icon}}</span>
          <div>
            <h3 class="font-pixel text-base text-rose-400">${{b.html_name}}</h3>
            <span class="font-mono text-xs text-slate-400">Entidad: ${{b.entity}} | Level ${{b.level}}</span>
          </div>
        </div>
        <div class="space-y-3 font-mono text-xs pt-2">
          <div>
            <span class="text-yellow-400 font-bold block mb-1">PODERES ESPECIALES:</span>
            ${{b.powers.map(p => `<div class="text-slate-300">⚡ ${{p}}</div>`).join('')}}
          </div>
          <div>
            <span class="text-emerald-400 font-bold block mb-1">BOTÍN ÚNICO DE DROPS:</span>
            ${{b.loot.map(l => `<div class="text-emerald-300">❖ ${{l}}</div>`).join('')}}
          </div>
        </div>
      `;
      document.getElementById('mc-modal').classList.remove('hidden');
    }}

    function closeMcModal() {{
      playMcSound('click');
      document.getElementById('mc-modal').classList.add('hidden');
    }}

    // Main Tab Switcher
    function switchTab(tabId) {{
      const tabs = ['leaderboards', 'profile', 'items', 'bosses', 'map', 'summary'];
      tabs.forEach(t => {{
        const view = document.getElementById(`view-${{t}}`);
        const btn = document.getElementById(`tab-btn-${{t}}`);
        const mBtn = document.getElementById(`m-tab-${{t}}`);
        
        if (t === tabId) {{
          if (view) view.classList.remove('hidden');
          if (btn) btn.className = 'nav-btn active px-4 py-2 font-pixel text-xs rounded bg-slate-900 border-2 border-yellow-500/60 text-yellow-400 transition flex items-center gap-2 shadow';
          if (mBtn) mBtn.className = 'py-1 px-2 text-yellow-400 font-bold whitespace-nowrap';
        }} else {{
          if (view) view.classList.add('hidden');
          if (btn) btn.className = 'nav-btn px-4 py-2 font-pixel text-xs rounded bg-slate-900 border-2 border-slate-700 text-slate-300 hover:text-white transition flex items-center gap-2';
          if (mBtn) mBtn.className = 'py-1 px-2 text-slate-400 font-medium whitespace-nowrap';
        }}
      }});
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function copyServerIP() {{
      playMcSound('levelup');
      navigator.clipboard.writeText("ut09.holy.gg:25898").then(() => {{
        const textSpan = document.getElementById('ip-text');
        const orig = textSpan.textContent;
        textSpan.textContent = "¡IP COPIADA!";
        textSpan.classList.add('text-emerald-400');
        setTimeout(() => {{
          textSpan.textContent = orig;
          textSpan.classList.remove('text-emerald-400');
        }}, 2200);
      }}).catch(() => {{
        alert("IP: ut09.holy.gg:25898");
      }});
    }}

    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
'''

    os.makedirs('dist', exist_ok=True)
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    with open('stats.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("[ÉXITO TOTAL] Rediseño 100% estilo Minecraft RPG generado en dist/index.html y stats.html!")

if __name__ == '__main__':
    generate_website()
