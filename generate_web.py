# -*- coding: utf-8 -*-
import json
import os

def generate_website():
    with open('dist/stats_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    json_str = json.dumps(data, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Holy Server RPG | Estadísticas & Leaderboards</title>
  <meta name="description" content="Panel de estadísticas, habilidades RPG AuraSkills, clasificaciones y mapa en vivo del servidor Minecraft Holy Server." />
  
  <!-- Tailwind CSS Play CDN & Fonts -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            display: ['"Outfit"', 'sans-serif']
          }},
          colors: {{
            mc: {{
              dark: '#080c14',
              card: '#0f172a',
              border: '#1e293b',
              gold: '#fbbf24',
              emerald: '#10b981',
              diamond: '#38bdf8',
              amethyst: '#c084fc',
              redstone: '#f43f5e'
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #080c14 45%, #05070d 100%);
      min-height: 100vh;
      color: #f1f5f9;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    .glass-card {{
      background: rgba(15, 23, 42, 0.78);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }}
    .glass-card:hover {{
      border-color: rgba(56, 189, 248, 0.25);
    }}
    .glow-gold {{
      box-shadow: 0 0 25px rgba(251, 191, 36, 0.2);
    }}
    .glow-emerald {{
      box-shadow: 0 0 25px rgba(16, 185, 129, 0.2);
    }}
    .glow-diamond {{
      box-shadow: 0 0 25px rgba(56, 189, 248, 0.2);
    }}
    .nav-btn.active {{
      background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(16, 185, 129, 0.15) 100%);
      color: #38bdf8;
      border-color: rgba(56, 189, 248, 0.4);
    }}
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
      width: 8px;
      height: 8px;
    }}
    ::-webkit-scrollbar-track {{
      background: #080c14;
    }}
    ::-webkit-scrollbar-thumb {{
      background: #1e293b;
      border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: #334155;
    }}
    @keyframes pulse-subtle {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.6; }}
    }}
    .pulse-dot {{
      animation: pulse-subtle 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }}
  </style>
</head>
<body class="antialiased selection:bg-cyan-500 selection:text-black">

  <!-- Top Announcement Bar / Server Status -->
  <header class="border-b border-white/5 bg-slate-950/60 backdrop-blur-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      
      <!-- Brand & Status -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-emerald-500 p-0.5 shadow-lg flex items-center justify-center">
          <span class="text-xl">⚔️</span>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="font-display font-extrabold text-lg tracking-wide text-white">HOLY SERVER <span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-400 to-emerald-400">RPG</span></h1>
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-950/80 text-emerald-400 border border-emerald-500/30">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 pulse-dot"></span> Online
            </span>
          </div>
          <p class="text-xs text-slate-400">Survival RPG con AuraSkills & Economia</p>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <nav class="hidden md:flex items-center gap-1.5 bg-slate-900/80 p-1.5 rounded-xl border border-white/5 text-sm font-medium">
        <button onclick="switchTab('leaderboards')" id="tab-btn-leaderboards" class="nav-btn active px-4 py-1.5 rounded-lg border border-transparent transition-all flex items-center gap-2">
          <span>🏆</span> Clasificación
        </button>
        <button onclick="switchTab('profile')" id="tab-btn-profile" class="nav-btn px-4 py-1.5 rounded-lg border border-transparent transition-all flex items-center gap-2 text-slate-300 hover:text-white">
          <span>👤</span> Jugadores
        </button>
        <button onclick="switchTab('map')" id="tab-btn-map" class="nav-btn px-4 py-1.5 rounded-lg border border-transparent transition-all flex items-center gap-2 text-slate-300 hover:text-white">
          <span>🗺️</span> Mapa en Vivo
        </button>
        <button onclick="switchTab('summary')" id="tab-btn-summary" class="nav-btn px-4 py-1.5 rounded-lg border border-transparent transition-all flex items-center gap-2 text-slate-300 hover:text-white">
          <span>📊</span> Estadísticas Globales
        </button>
      </nav>

      <!-- Server IP Copy Button -->
      <div class="flex items-center gap-2">
        <button onclick="copyServerIP()" id="btn-copy-ip" class="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition shadow-sm active:scale-95">
          <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
          <span id="ip-text">ut09.holy.gg:25898</span>
        </button>
      </div>

    </div>

    <!-- Mobile Nav Bar -->
    <div class="md:hidden flex items-center justify-around border-t border-white/5 bg-slate-950/90 p-2 text-xs">
      <button onclick="switchTab('leaderboards')" id="m-tab-leaderboards" class="py-1 px-3 text-cyan-400 font-medium">🏆 Top</button>
      <button onclick="switchTab('profile')" id="m-tab-profile" class="py-1 px-3 text-slate-400 font-medium">👤 Perfiles</button>
      <button onclick="switchTab('map')" id="m-tab-map" class="py-1 px-3 text-slate-400 font-medium">🗺️ Mapa</button>
      <button onclick="switchTab('summary')" id="m-tab-summary" class="py-1 px-3 text-slate-400 font-medium">📊 Servidor</button>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

    <!-- ========================================== -->
    <!-- TAB 1: CLASIFICACION / LEADERBOARDS       -->
    <!-- ========================================== -->
    <section id="view-leaderboards" class="space-y-8">
      
      <!-- Leaderboard Header Banner -->
      <div class="relative overflow-hidden rounded-3xl glass-card p-6 md:p-10 border border-amber-500/20">
        <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-amber-400/10 text-amber-300 border border-amber-400/20 mb-3">
              <span>⭐</span> Ranking Oficial del Servidor
            </div>
            <h2 class="font-display font-extrabold text-3xl sm:text-4xl text-white tracking-tight">Tabla de Clasificación General</h2>
            <p class="text-slate-400 text-sm sm:text-base mt-2 max-w-2xl">
              Descubre quiénes lideran las habilidades RPG de AuraSkills, el tiempo jugado, los monstruos derrotados y los bloques minados en la comunidad.
            </p>
          </div>

          <!-- Quick Stat Counters -->
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
            <div class="bg-slate-900/90 border border-white/5 rounded-2xl p-3.5 text-center">
              <span class="text-xs text-slate-400 font-medium block">Jugadores Registrados</span>
              <span id="lb-total-players" class="font-display font-black text-2xl text-cyan-400">13</span>
            </div>
            <div class="bg-slate-900/90 border border-white/5 rounded-2xl p-3.5 text-center">
              <span class="text-xs text-slate-400 font-medium block">Horas Totales</span>
              <span id="lb-total-hours" class="font-display font-black text-2xl text-amber-400">58.9h</span>
            </div>
            <div class="col-span-2 sm:col-span-1 bg-slate-900/90 border border-white/5 rounded-2xl p-3.5 text-center">
              <span class="text-xs text-slate-400 font-medium block">Mobs Eliminados</span>
              <span id="lb-total-mobs" class="font-display font-black text-2xl text-emerald-400">2,266</span>
            </div>
          </div>
        </div>

        <!-- Leaderboard Category Filter Pills -->
        <div class="mt-8 flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none" id="lb-pills">
          <button onclick="setLeaderboardCategory('auraskills')" class="lb-pill active px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 shadow-md">
            ✨ AuraSkills RPG
          </button>
          <button onclick="setLeaderboardCategory('play_time')" class="lb-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5">
            ⏱️ Tiempo Jugado
          </button>
          <button onclick="setLeaderboardCategory('mob_kills')" class="lb-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5">
            ⚔️ Mobs Asesinados
          </button>
          <button onclick="setLeaderboardCategory('player_kills')" class="lb-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5">
            🎯 PvP Kills
          </button>
          <button onclick="setLeaderboardCategory('mined')" class="lb-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5">
            ⛏️ Bloques Minados
          </button>
          <button onclick="setLeaderboardCategory('crafted')" class="lb-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5">
            🔨 Crafteos
          </button>
          <button onclick="setLeaderboardCategory('distance')" class="lb-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5">
            🧭 Exploración (Km)
          </button>
          <button onclick="setLeaderboardCategory('kdr')" class="lb-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5">
            💀 Ratio K/D
          </button>
        </div>
      </div>

      <!-- Top 3 Podium Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-end pt-4" id="podium-container">
        <!-- Rendered dynamically by JS -->
      </div>

      <!-- Full Ranking Table -->
      <div class="glass-card rounded-2xl overflow-hidden border border-white/5 shadow-2xl">
        <div class="px-6 py-4 border-b border-white/5 bg-slate-900/60 flex items-center justify-between">
          <h3 class="font-display font-bold text-base text-white flex items-center gap-2">
            <span>📋</span> Todos los Participantes
          </h3>
          <span class="text-xs text-slate-400">Haz clic en cualquier jugador para ver su perfil completo</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse text-sm">
            <thead>
              <tr class="border-b border-white/5 bg-slate-950/40 text-xs font-semibold uppercase tracking-wider text-slate-400">
                <th class="py-3.5 px-6">Posición</th>
                <th class="py-3.5 px-6">Jugador</th>
                <th class="py-3.5 px-6 text-right" id="table-score-col-title">Puntaje</th>
                <th class="py-3.5 px-6 text-center">Acción</th>
              </tr>
            </thead>
            <tbody id="leaderboard-table-body" class="divide-y divide-white/5">
              <!-- Rendered by JS -->
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- ========================================== -->
    <!-- TAB 2: PERFIL DE JUGADOR                  -->
    <!-- ========================================== -->
    <section id="view-profile" class="space-y-8 hidden">
      
      <!-- Player Selection & Search Bar -->
      <div class="glass-card rounded-2xl p-4 sm:p-6 border border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Seleccionar Jugador:</label>
          <div class="relative min-w-[280px]">
            <select id="player-select" onchange="onPlayerSelectChange(this.value)" class="w-full appearance-none bg-slate-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm font-semibold text-white focus:outline-none focus:border-cyan-500 cursor-pointer shadow-inner pr-10">
              <!-- Options populated by JS -->
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </div>
          </div>
        </div>

        <!-- Quick player search input -->
        <div class="w-full sm:w-72">
          <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">Buscar por nombre:</label>
          <input type="text" id="player-search-input" onkeyup="filterPlayerDropdown(this.value)" placeholder="Ej. Stargolden, Kiruao..." class="w-full bg-slate-900/90 border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 shadow-inner">
        </div>
      </div>

      <!-- Player Header Card -->
      <div class="glass-card rounded-3xl p-6 sm:p-8 border border-white/10 relative overflow-hidden">
        <div class="absolute -right-16 -top-16 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="flex flex-col md:flex-row items-center gap-6 relative z-10">
          
          <!-- Avatar Frame -->
          <div class="relative group">
            <div class="w-28 h-28 sm:w-32 sm:h-32 rounded-2xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-amber-500 p-1 shadow-2xl">
              <img id="p-avatar" src="" alt="Avatar" class="w-full h-full object-cover rounded-xl bg-slate-900 shadow-inner" onerror="this.src='https://minotar.net/helm/Steve/100.png'">
            </div>
            <span id="p-bedrock-badge" class="hidden absolute -bottom-2 -right-2 bg-gradient-to-r from-red-600 to-amber-600 text-white text-[10px] font-extrabold px-2 py-0.5 rounded-full shadow-md border border-white/20 uppercase">
              Bedrock
            </span>
          </div>

          <!-- Player Meta -->
          <div class="text-center md:text-left space-y-1.5 flex-1">
            <div class="flex flex-wrap items-center justify-center md:justify-start gap-2">
              <h2 id="p-name" class="font-display font-black text-3xl sm:text-4xl text-white tracking-wide">Stargolden</h2>
              <span id="p-rank-badge" class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                ⭐ Nivel AuraSkills: <span id="p-total-skills-badge">0</span>
              </span>
            </div>
            <p class="text-xs text-slate-400 font-mono flex items-center justify-center md:justify-start gap-1">
              <span>UUID:</span> <span id="p-uuid" class="text-slate-300">f0d03f69-7585-3e09-aaaa-cba59086d8db</span>
            </p>
            <div class="pt-2 flex flex-wrap items-center justify-center md:justify-start gap-2 text-xs">
              <span class="px-3 py-1 rounded-xl bg-slate-800/90 text-cyan-300 border border-cyan-500/20 font-medium flex items-center gap-1.5">
                ⏱️ Tiempo: <strong id="p-playtime" class="text-white">0h</strong>
              </span>
              <span class="px-3 py-1 rounded-xl bg-slate-800/90 text-emerald-300 border border-emerald-500/20 font-medium flex items-center gap-1.5">
                🧪 Maná: <strong id="p-mana" class="text-white">0</strong>
              </span>
              <span class="px-3 py-1 rounded-xl bg-slate-800/90 text-amber-300 border border-amber-500/20 font-medium flex items-center gap-1.5">
                🏆 Logros: <strong id="p-advancements" class="text-white">0</strong>
              </span>
            </div>
          </div>

          <!-- Quick Stat Cards -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 w-full md:w-auto">
            <div class="bg-slate-900/90 border border-white/5 rounded-2xl p-3 text-center min-w-[100px]">
              <span class="text-[11px] text-slate-400 font-semibold block uppercase">Mobs Kills</span>
              <span id="p-mobkills" class="font-display font-black text-xl text-emerald-400">0</span>
            </div>
            <div class="bg-slate-900/90 border border-white/5 rounded-2xl p-3 text-center min-w-[100px]">
              <span class="text-[11px] text-slate-400 font-semibold block uppercase">Muertes</span>
              <span id="p-deaths" class="font-display font-black text-xl text-rose-400">0</span>
            </div>
            <div class="bg-slate-900/90 border border-white/5 rounded-2xl p-3 text-center min-w-[100px]">
              <span class="text-[11px] text-slate-400 font-semibold block uppercase">K/D Ratio</span>
              <span id="p-kdr" class="font-display font-black text-xl text-cyan-400">0.0</span>
            </div>
            <div class="bg-slate-900/90 border border-white/5 rounded-2xl p-3 text-center min-w-[100px]">
              <span class="text-[11px] text-slate-400 font-semibold block uppercase">PvP Kills</span>
              <span id="p-playerkills" class="font-display font-black text-xl text-amber-400">0</span>
            </div>
          </div>

        </div>
      </div>

      <!-- AURASKILLS RPG SECTION -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-2xl">✨</span>
            <h3 class="font-display font-extrabold text-2xl text-white">Habilidades AuraSkills RPG</h3>
          </div>
          <div class="text-xs sm:text-sm text-slate-400">
            Nivel Promedio: <strong id="p-skill-average" class="text-amber-400 text-base font-bold">0.0</strong>
          </div>
        </div>

        <!-- 11 Skills Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4" id="skills-grid">
          <!-- Populated by JS -->
        </div>
      </div>

      <!-- STATS TABS / GRIDS: Combat, Mining, Distances -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Bloques Minados -->
        <div class="glass-card rounded-2xl p-6 border border-white/5 space-y-4">
          <div class="flex items-center justify-between border-b border-white/5 pb-3">
            <h4 class="font-display font-bold text-lg text-white flex items-center gap-2">
              <span>⛏️</span> Top Bloques Minados
            </h4>
            <span class="text-xs font-semibold px-2.5 py-1 rounded-lg bg-cyan-950 text-cyan-400 border border-cyan-500/30" id="p-total-mined">
              0 en total
            </span>
          </div>
          <div class="space-y-2.5" id="p-mined-list">
            <!-- Populated by JS -->
          </div>
        </div>

        <!-- Items Crafteados -->
        <div class="glass-card rounded-2xl p-6 border border-white/5 space-y-4">
          <div class="flex items-center justify-between border-b border-white/5 pb-3">
            <h4 class="font-display font-bold text-lg text-white flex items-center gap-2">
              <span>🔨</span> Top Items Fabricados
            </h4>
            <span class="text-xs font-semibold px-2.5 py-1 rounded-lg bg-amber-950 text-amber-400 border border-amber-500/30" id="p-total-crafted">
              0 en total
            </span>
          </div>
          <div class="space-y-2.5" id="p-crafted-list">
            <!-- Populated by JS -->
          </div>
        </div>

        <!-- Mobs Asesinados -->
        <div class="glass-card rounded-2xl p-6 border border-white/5 space-y-4">
          <div class="flex items-center justify-between border-b border-white/5 pb-3">
            <h4 class="font-display font-bold text-lg text-white flex items-center gap-2">
              <span>⚔️</span> Bestiario / Mobs Derrotados
            </h4>
            <span class="text-xs text-slate-400">Total eliminados</span>
          </div>
          <div class="space-y-2.5" id="p-mobs-list">
            <!-- Populated by JS -->
          </div>
        </div>

        <!-- Exploración y Distancias -->
        <div class="glass-card rounded-2xl p-6 border border-white/5 space-y-4">
          <div class="flex items-center justify-between border-b border-white/5 pb-3">
            <h4 class="font-display font-bold text-lg text-white flex items-center gap-2">
              <span>🧭</span> Distancias Recorridas
            </h4>
            <span class="text-xs font-semibold px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-500/30" id="p-total-distance">
              0 km
            </span>
          </div>
          
          <div class="grid grid-cols-2 gap-3" id="p-distances-grid">
            <!-- Populated by JS -->
          </div>

          <!-- Causas de muerte -->
          <div class="border-t border-white/5 pt-4">
            <h5 class="text-xs font-bold uppercase tracking-wider text-rose-400 mb-3 flex items-center gap-1.5">
              <span>💀</span> Causas de Muerte
            </h5>
            <div class="space-y-2" id="p-deaths-by-list">
              <!-- Populated by JS -->
            </div>
          </div>

        </div>

      </div>

    </section>

    <!-- ========================================== -->
    <!-- TAB 3: MAPA EN VIVO                       -->
    <!-- ========================================== -->
    <section id="view-map" class="space-y-6 hidden">
      
      <!-- Map Hub Hero Banner -->
      <div class="glass-card rounded-3xl p-6 sm:p-8 border border-cyan-500/20 relative overflow-hidden">
        <div class="absolute -right-16 -bottom-16 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div class="space-y-2 max-w-2xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-cyan-400/10 text-cyan-300 border border-cyan-400/20">
              <span class="w-2 h-2 rounded-full bg-cyan-400 pulse-dot"></span> Visor 3D BlueMap en Tiempo Real
            </div>
            <h3 class="font-display font-black text-3xl sm:text-4xl text-white tracking-wide">
              Mapa del Mundo en Vivo
            </h3>
            <p class="text-slate-400 text-sm">
              Explora construcciones, biomas, mazmorras y la ubicación en vivo de todos los jugadores conectados en perspectiva 3D isométrica y primera persona.
            </p>
          </div>

          <!-- Big Action Button -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <a href="http://ut09.holy.gg:25898/" target="_blank" rel="noopener noreferrer" class="px-6 py-3.5 rounded-2xl bg-gradient-to-r from-cyan-500 to-emerald-500 hover:from-cyan-400 hover:to-emerald-400 text-slate-950 font-display font-black text-sm transition transform hover:scale-105 shadow-xl shadow-cyan-500/25 flex items-center justify-center gap-2 text-center">
              <span>🚀</span> Abrir Visor 3D en Pantalla Completa <span>↗</span>
            </a>
          </div>
        </div>

        <!-- Browser HTTPS Note -->
        <div class="mt-6 pt-4 border-t border-white/5 flex items-start gap-3 text-xs text-slate-400 bg-slate-900/60 p-3.5 rounded-xl border border-white/5">
          <span class="text-amber-400 text-base">ℹ️</span>
          <div>
            <strong class="text-slate-200">¿Por qué abrirlo en nueva pestaña?</strong> Los navegadores modernos bloquean visores embebidos por seguridad cuando la web está en HTTPS y el servidor del mapa en HTTP. Al abrirlo directamente en nueva pestaña, carga a máxima velocidad y con aceleración 3D por hardware.
          </div>
        </div>
      </div>

      <!-- Feature Highlights Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="glass-card rounded-2xl p-5 border border-white/5 space-y-1.5">
          <div class="text-2xl mb-1">🎮</div>
          <h4 class="font-bold text-white text-sm">3 Modos de Cámara</h4>
          <p class="text-xs text-slate-400">Perspectiva libre, vista ortográfica cenital y modo primera persona como si estuvieras en el juego.</p>
        </div>

        <div class="glass-card rounded-2xl p-5 border border-white/5 space-y-1.5">
          <div class="text-2xl mb-1">👥</div>
          <h4 class="font-bold text-white text-sm">Rastreo de Jugadores</h4>
          <p class="text-xs text-slate-400">Mira dónde están tus amigos en el mapa con su skin real y coordenadas actualizadas al segundo.</p>
        </div>

        <div class="glass-card rounded-2xl p-5 border border-white/5 space-y-1.5">
          <div class="text-2xl mb-1">🏰</div>
          <h4 class="font-bold text-white text-sm">Marcadores y Zonas</h4>
          <p class="text-xs text-slate-400">Spawn principal, tiendas, portales y zonas protegidas señalizadas con iconos personalizados.</p>
        </div>
      </div>

      <!-- Interactive Embedded Viewer Box -->
      <div class="glass-card rounded-3xl overflow-hidden border border-white/10 relative shadow-2xl" style="height: 680px;">
        <div class="p-3 bg-slate-900/80 border-b border-white/5 flex items-center justify-between text-xs text-slate-400">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 rounded-full bg-rose-500/80 inline-block"></span>
            <span class="w-3 h-3 rounded-full bg-amber-500/80 inline-block"></span>
            <span class="w-3 h-3 rounded-full bg-emerald-500/80 inline-block"></span>
            <span class="font-mono text-[11px] text-slate-300 ml-2">http://ut09.holy.gg:25898/</span>
          </div>
          <a href="http://ut09.holy.gg:25898/" target="_blank" class="text-cyan-400 hover:underline flex items-center gap-1 font-semibold">
            Abrir fuera ↗
          </a>
        </div>
        <iframe id="map-iframe" src="http://ut09.holy.gg:25898/" class="w-full h-full border-0" allowfullscreen sandbox="allow-scripts allow-same-origin allow-popups"></iframe>
      </div>

    </section>

    <!-- ========================================== -->
    <!-- TAB 4: ESTADÍSTICAS GLOBALES DEL SERVIDOR -->
    <!-- ========================================== -->
    <section id="view-summary" class="space-y-8 hidden">
      <div class="glass-card rounded-3xl p-8 border border-white/10 relative overflow-hidden">
        <div class="relative z-10 max-w-3xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-400/10 text-emerald-300 border border-emerald-400/20 mb-3">
            <span>🌐</span> Comunidad Activa
          </div>
          <h2 class="font-display font-extrabold text-3xl sm:text-4xl text-white">Impacto Global de la Comunidad</h2>
          <p class="text-slate-400 text-sm sm:text-base mt-2">
            La suma de cada bloque roto, cada aventura, cada dragón o mob vencido y cada paso dado en el servidor Holy.
          </p>
        </div>
      </div>

      <!-- Big Metric Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="glass-card rounded-2xl p-6 border border-white/5 space-y-2">
          <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider">
            <span>Tiempo Comunitario</span>
            <span class="text-xl">⏳</span>
          </div>
          <div class="font-display font-black text-3xl text-amber-400" id="g-hours">0h</div>
          <p class="text-xs text-slate-500">Horas acumuladas de todos los miembros</p>
        </div>

        <div class="glass-card rounded-2xl p-6 border border-white/5 space-y-2">
          <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider">
            <span>Bloques Minados</span>
            <span class="text-xl">⛏️</span>
          </div>
          <div class="font-display font-black text-3xl text-cyan-400" id="g-mined">0</div>
          <p class="text-xs text-slate-500">Piedra, minerales y escombros rotos</p>
        </div>

        <div class="glass-card rounded-2xl p-6 border border-white/5 space-y-2">
          <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider">
            <span>Monstruos Derrotados</span>
            <span class="text-xl">⚔️</span>
          </div>
          <div class="font-display font-black text-3xl text-emerald-400" id="g-mobs">0</div>
          <p class="text-xs text-slate-500">Criaturas hostiles erradicadas</p>
        </div>

        <div class="glass-card rounded-2xl p-6 border border-white/5 space-y-2">
          <div class="flex items-center justify-between text-slate-400 text-xs font-bold uppercase tracking-wider">
            <span>Distancia Explorada</span>
            <span class="text-xl">🧭</span>
          </div>
          <div class="font-display font-black text-3xl text-indigo-400" id="g-dist">0 km</div>
          <p class="text-xs text-slate-500">Kilómetros viajados a pie, bote y caballo</p>
        </div>
      </div>

      <!-- Server Connection Instructions Card -->
      <div class="glass-card rounded-2xl p-8 border border-white/5 space-y-6">
        <h3 class="font-display font-bold text-xl text-white">¿Cómo unirse al servidor?</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
          <div class="bg-slate-900/60 p-5 rounded-2xl border border-white/5 space-y-2">
            <h4 class="font-bold text-cyan-400 flex items-center gap-2">
              <span>☕</span> Minecraft Java Edition
            </h4>
            <p class="text-slate-400 text-xs">
              Versión recomendada: <strong>1.21+</strong>. Abre Minecraft, ve a Multijugador &gt; Añadir Servidor y coloca la siguiente dirección:
            </p>
            <div class="font-mono bg-slate-950 px-3 py-2 rounded-xl text-emerald-400 font-bold text-xs select-all border border-emerald-500/20">
              ut09.holy.gg:25898
            </div>
          </div>

          <div class="bg-slate-900/60 p-5 rounded-2xl border border-white/5 space-y-2">
            <h4 class="font-bold text-amber-400 flex items-center gap-2">
              <span>📱</span> Minecraft Bedrock Edition (GeyserMC)
            </h4>
            <p class="text-slate-400 text-xs">
              Móvil, Windows 10/11, Switch o Consolas. Conéctate con:
            </p>
            <div class="font-mono bg-slate-950 px-3 py-2 rounded-xl text-amber-300 font-bold text-xs select-all border border-amber-500/20">
              IP: ut09.holy.gg | Puerto: 25898
            </div>
          </div>
        </div>
      </div>

    </section>

  </main>

  <!-- Footer -->
  <footer class="border-t border-white/5 bg-slate-950/80 py-8 mt-12 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
      <p>Holy Server RPG &copy; 2026. Todos los derechos reservados.</p>
      <p class="flex items-center gap-2">
        <span>Alojado en Cloudflare Pages</span> • 
        <span class="text-emerald-400">Protección DDoS & CDN Global</span>
      </p>
    </div>
  </footer>

  <!-- Embedded Dataset (Allows running via file:// or http:// with zero CORS issues) -->
  <script id="embedded-data" type="application/json">
{json_str}
  </script>

  <!-- Application Logic -->
  <script>
    // State
    let APP_DATA = null;
    let CURRENT_LEADERBOARD_CAT = 'auraskills';
    let CURRENT_PLAYER_UUID = null;

    // Initialize App
    function init() {{
      try {{
        const raw = document.getElementById('embedded-data').textContent;
        APP_DATA = JSON.parse(raw);
      }} catch (e) {{
        console.error("Error loading embedded data:", e);
      }}

      if (!APP_DATA || !APP_DATA.players || APP_DATA.players.length === 0) {{
        alert("No se pudieron cargar las estadísticas.");
        return;
      }}

      // Init Summary
      initSummary();

      // Init Leaderboards
      renderLeaderboard(CURRENT_LEADERBOARD_CAT);

      // Init Players Select
      initPlayerDropdown();

      // Select default player (Stargolden or top player)
      const defaultPlayer = APP_DATA.players.find(p => p.name.toLowerCase() === 'stargolden') || APP_DATA.players[0];
      if (defaultPlayer) {{
        renderPlayerProfile(defaultPlayer.uuid);
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

    // Leaderboard Tabs & Categories
    const LB_CONFIG = {{
      auraskills: {{ title: 'Nivel Total AuraSkills', icon: '✨', pillColor: 'from-amber-500 to-amber-600' }},
      play_time: {{ title: 'Tiempo Jugado', icon: '⏱️', pillColor: 'from-cyan-500 to-cyan-600' }},
      mob_kills: {{ title: 'Mobs Eliminados', icon: '⚔️', pillColor: 'from-emerald-500 to-emerald-600' }},
      player_kills: {{ title: 'PvP Kills', icon: '🎯', pillColor: 'from-rose-500 to-rose-600' }},
      mined: {{ title: 'Bloques Minados', icon: '⛏️', pillColor: 'from-amber-500 to-orange-600' }},
      crafted: {{ title: 'Items Crafteados', icon: '🔨', pillColor: 'from-yellow-500 to-amber-600' }},
      distance: {{ title: 'Distancia Recorrida', icon: '🧭', pillColor: 'from-indigo-500 to-purple-600' }},
      kdr: {{ title: 'K/D Ratio', icon: '💀', pillColor: 'from-fuchsia-500 to-pink-600' }}
    }};

    function setLeaderboardCategory(cat) {{
      CURRENT_LEADERBOARD_CAT = cat;
      
      // Update pills
      const buttons = document.querySelectorAll('#lb-pills button');
      buttons.forEach(b => {{
        b.className = 'lb-pill px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-slate-800 hover:bg-slate-700 text-slate-300 border border-white/5';
      }});
      event.currentTarget.className = 'lb-pill active px-4 py-2 rounded-xl text-xs sm:text-sm font-semibold whitespace-nowrap transition-all bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 shadow-md font-bold';

      renderLeaderboard(cat);
    }}

    function renderLeaderboard(cat) {{
      const list = APP_DATA.leaderboards[cat] || [];
      const config = LB_CONFIG[cat] || {{ title: 'Puntos', icon: '⭐' }};
      document.getElementById('table-score-col-title').textContent = config.title;

      // Podium Top 3
      const podium = document.getElementById('podium-container');
      podium.innerHTML = '';

      const top1 = list[0];
      const top2 = list[1];
      const top3 = list[2];

      const podiumItems = [
        {{ p: top2, rank: 2, trophy: '🥈', color: 'slate-300', border: 'border-slate-400/40', bg: 'bg-slate-800/40', order: 'order-2 md:order-1' }},
        {{ p: top1, rank: 1, trophy: '👑', color: 'amber-400', border: 'border-amber-400/60 shadow-amber-500/20 shadow-2xl', bg: 'bg-amber-950/30', order: 'order-1 md:order-2 -mt-4' }},
        {{ p: top3, rank: 3, trophy: '🥉', color: 'amber-600', border: 'border-amber-700/40', bg: 'bg-amber-950/20', order: 'order-3' }}
      ];

      podiumItems.forEach(item => {{
        if (!item.p) return;
        const card = document.createElement('div');
        card.className = `${{item.order}} glass-card rounded-2xl p-6 text-center border ${{item.border}} ${{item.bg}} relative transition-transform hover:-translate-y-1.5 cursor-pointer`;
        card.onclick = () => viewPlayerProfileFromList(item.p.uuid);

        card.innerHTML = `
          <div class="absolute -top-3 left-1/2 -translate-x-1/2 text-2xl font-black">${{item.trophy}}</div>
          <div class="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-tr from-cyan-500 to-emerald-500 p-0.5 shadow-lg mt-2 mb-3">
            <img src="${{item.p.avatar}}" class="w-full h-full rounded-xl bg-slate-900 object-cover" onerror="this.src='https://minotar.net/helm/Steve/100.png'">
          </div>
          <h4 class="font-display font-extrabold text-lg text-white truncate">${{item.p.name}}</h4>
          <span class="text-xs font-semibold text-${{item.color}} block mt-1">${{item.p.score}}</span>
          <div class="mt-4 pt-3 border-t border-white/5 text-[11px] text-cyan-400 font-semibold flex items-center justify-center gap-1">
            Ver Perfil <span>&rarr;</span>
          </div>
        `;
        podium.appendChild(card);
      }});

      // Full table
      const tbody = document.getElementById('leaderboard-table-body');
      tbody.innerHTML = '';

      list.forEach((p, idx) => {{
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-800/40 transition cursor-pointer';
        tr.onclick = () => viewPlayerProfileFromList(p.uuid);

        let rankBadge = `<span class="font-display font-bold text-slate-400">#${{idx + 1}}</span>`;
        if (idx === 0) rankBadge = `<span class="inline-flex items-center justify-center w-7 h-7 rounded-full bg-amber-400/20 text-amber-400 font-black text-xs border border-amber-400/40">1</span>`;
        if (idx === 1) rankBadge = `<span class="inline-flex items-center justify-center w-7 h-7 rounded-full bg-slate-400/20 text-slate-300 font-black text-xs border border-slate-400/40">2</span>`;
        if (idx === 2) rankBadge = `<span class="inline-flex items-center justify-center w-7 h-7 rounded-full bg-amber-700/20 text-amber-500 font-black text-xs border border-amber-700/40">3</span>`;

        tr.innerHTML = `
          <td class="py-3.5 px-6 whitespace-nowrap">${{rankBadge}}</td>
          <td class="py-3.5 px-6 whitespace-nowrap">
            <div class="flex items-center gap-3">
              <img src="${{p.avatar}}" class="w-8 h-8 rounded-lg bg-slate-800 object-cover" onerror="this.src='https://minotar.net/helm/Steve/100.png'">
              <span class="font-bold text-white hover:text-cyan-400 transition">${{p.name}}</span>
            </div>
          </td>
          <td class="py-3.5 px-6 whitespace-nowrap text-right font-display font-extrabold text-cyan-300">${{p.score}}</td>
          <td class="py-3.5 px-6 whitespace-nowrap text-center">
            <button class="px-3 py-1 rounded-lg bg-slate-800 hover:bg-cyan-600 text-slate-300 hover:text-white text-xs font-semibold transition border border-white/5">
              Ver Perfil
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
        opt.textContent = `${{p.name}} (${{p.play_time_str}}) - AuraSkills: Lvl ${{p.total_skill_level}}`;
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
      renderPlayerProfile(uuid);
    }}

    function viewPlayerProfileFromList(uuid) {{
      switchTab('profile');
      const select = document.getElementById('player-select');
      select.value = uuid;
      renderPlayerProfile(uuid);
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    function renderPlayerProfile(uuid) {{
      CURRENT_PLAYER_UUID = uuid;
      const p = APP_DATA.players.find(x => x.uuid === uuid);
      if (!p) return;

      // Header Meta
      document.getElementById('p-avatar').src = p.avatar;
      document.getElementById('p-name').textContent = p.name;
      document.getElementById('p-uuid').textContent = p.uuid;
      document.getElementById('p-total-skills-badge').textContent = p.total_skill_level;
      document.getElementById('p-playtime').textContent = p.play_time_str;
      document.getElementById('p-mana').textContent = p.mana;
      document.getElementById('p-advancements').textContent = p.advancements_count;

      const bedrockBadge = document.getElementById('p-bedrock-badge');
      if (p.is_bedrock) {{
        bedrockBadge.classList.remove('hidden');
      }} else {{
        bedrockBadge.classList.add('hidden');
      }}

      // Quick Stat Numbers
      document.getElementById('p-mobkills').textContent = p.mob_kills.toLocaleString();
      document.getElementById('p-deaths').textContent = p.deaths.toLocaleString();
      document.getElementById('p-kdr').textContent = p.kdr.toFixed(2);
      document.getElementById('p-playerkills').textContent = p.player_kills.toLocaleString();

      // AuraSkills RPG
      document.getElementById('p-skill-average').textContent = p.skill_average.toFixed(1);
      const skillsGrid = document.getElementById('skills-grid');
      skillsGrid.innerHTML = '';

      p.skills.forEach(s => {{
        const card = document.createElement('div');
        card.className = 'glass-card rounded-2xl p-4 border border-white/5 space-y-2 hover:border-amber-500/30 transition';
        
        // Calculate max xp approx for visual progress bar
        const maxLevel = 100;
        const progressPct = Math.min(100, Math.round((s.level / 20) * 100));

        card.innerHTML = `
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-xl">${{s.icon}}</span>
              <span class="font-bold text-sm text-white">${{s.name}}</span>
            </div>
            <span class="font-display font-black text-amber-400 text-base">Lvl ${{s.level}}</span>
          </div>
          <div class="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-white/5">
            <div class="bg-gradient-to-r from-amber-500 to-emerald-400 h-2 rounded-full transition-all duration-500" style="width: ${{progressPct}}%"></div>
          </div>
          <div class="flex items-center justify-between text-[11px] text-slate-400 font-mono">
            <span>XP: ${{s.xp.toLocaleString()}}</span>
            <span>${{progressPct}}%</span>
          </div>
        `;
        skillsGrid.appendChild(card);
      }});

      // Top Mined
      document.getElementById('p-total-mined').textContent = p.total_mined.toLocaleString() + ' en total';
      const minedList = document.getElementById('p-mined-list');
      minedList.innerHTML = '';
      if (p.top_mined.length === 0) {{
        minedList.innerHTML = '<p class="text-xs text-slate-500 italic">No ha minado bloques aún.</p>';
      }} else {{
        p.top_mined.forEach(m => {{
          const item = document.createElement('div');
          item.className = 'flex items-center justify-between p-2.5 rounded-xl bg-slate-900/60 border border-white/5 text-xs';
          item.innerHTML = `
            <span class="font-semibold text-slate-200 truncate pr-2">${{m.name}}</span>
            <span class="font-mono font-bold text-cyan-400">${{m.count.toLocaleString()}}</span>
          `;
          minedList.appendChild(item);
        }});
      }}

      // Top Crafted
      document.getElementById('p-total-crafted').textContent = p.total_crafted.toLocaleString() + ' en total';
      const craftedList = document.getElementById('p-crafted-list');
      craftedList.innerHTML = '';
      if (p.top_crafted.length === 0) {{
        craftedList.innerHTML = '<p class="text-xs text-slate-500 italic">No ha fabricado items aún.</p>';
      }} else {{
        p.top_crafted.forEach(m => {{
          const item = document.createElement('div');
          item.className = 'flex items-center justify-between p-2.5 rounded-xl bg-slate-900/60 border border-white/5 text-xs';
          item.innerHTML = `
            <span class="font-semibold text-slate-200 truncate pr-2">${{m.name}}</span>
            <span class="font-mono font-bold text-amber-400">${{m.count.toLocaleString()}}</span>
          `;
          craftedList.appendChild(item);
        }});
      }}

      // Mobs Killed
      const mobsList = document.getElementById('p-mobs-list');
      mobsList.innerHTML = '';
      if (p.top_mobs_killed.length === 0) {{
        mobsList.innerHTML = '<p class="text-xs text-slate-500 italic">No ha eliminado criaturas aún.</p>';
      }} else {{
        p.top_mobs_killed.forEach(m => {{
          const item = document.createElement('div');
          item.className = 'flex items-center justify-between p-2.5 rounded-xl bg-slate-900/60 border border-white/5 text-xs';
          item.innerHTML = `
            <span class="font-semibold text-slate-200 truncate pr-2">${{m.name}}</span>
            <span class="font-mono font-bold text-emerald-400">${{m.count.toLocaleString()}}</span>
          `;
          mobsList.appendChild(item);
        }});
      }}

      // Distances
      document.getElementById('p-total-distance').textContent = p.distances.total_km + ' km';
      const distGrid = document.getElementById('p-distances-grid');
      distGrid.innerHTML = `
        <div class="bg-slate-900/60 p-3 rounded-xl border border-white/5">
          <span class="text-[11px] text-slate-400 block font-medium">🚶 Caminando</span>
          <strong class="text-white text-sm">${{p.distances.walk_km}} km</strong>
        </div>
        <div class="bg-slate-900/60 p-3 rounded-xl border border-white/5">
          <span class="text-[11px] text-slate-400 block font-medium">🏃 Corriendo</span>
          <strong class="text-white text-sm">${{p.distances.sprint_km}} km</strong>
        </div>
        <div class="bg-slate-900/60 p-3 rounded-xl border border-white/5">
          <span class="text-[11px] text-slate-400 block font-medium">⛵ En Bote</span>
          <strong class="text-white text-sm">${{p.distances.boat_km}} km</strong>
        </div>
        <div class="bg-slate-900/60 p-3 rounded-xl border border-white/5">
          <span class="text-[11px] text-slate-400 block font-medium">🐎 A Caballo</span>
          <strong class="text-white text-sm">${{p.distances.horse_km}} km</strong>
        </div>
      `;

      // Deaths by
      const deathsByList = document.getElementById('p-deaths-by-list');
      deathsByList.innerHTML = '';
      if (p.deaths_by.length === 0) {{
        deathsByList.innerHTML = '<p class="text-xs text-slate-500 italic">Sin muertes registradas por monstruos.</p>';
      }} else {{
        p.deaths_by.forEach(d => {{
          const item = document.createElement('div');
          item.className = 'flex items-center justify-between p-2 rounded-xl bg-slate-950 border border-white/5 text-xs';
          item.innerHTML = `
            <span class="text-slate-300">${{d.name}}</span>
            <span class="font-mono text-rose-400 font-bold">${{d.count}}</span>
          `;
          deathsByList.appendChild(item);
        }});
      }}
    }}

    // Switch Main Tabs
    function switchTab(tabId) {{
      const tabs = ['leaderboards', 'profile', 'map', 'summary'];
      tabs.forEach(t => {{
        const view = document.getElementById(`view-${{t}}`);
        const btn = document.getElementById(`tab-btn-${{t}}`);
        const mBtn = document.getElementById(`m-tab-${{t}}`);
        
        if (t === tabId) {{
          view.classList.remove('hidden');
          if (btn) btn.className = 'nav-btn active px-4 py-1.5 rounded-lg border border-transparent transition-all flex items-center gap-2';
          if (mBtn) mBtn.className = 'py-1 px-3 text-cyan-400 font-medium';
        }} else {{
          view.classList.add('hidden');
          if (btn) btn.className = 'nav-btn px-4 py-1.5 rounded-lg border border-transparent transition-all flex items-center gap-2 text-slate-300 hover:text-white';
          if (mBtn) mBtn.className = 'py-1 px-3 text-slate-400 font-medium';
        }}
      }});
    }}

    // Copy Server IP
    function copyServerIP() {{
      navigator.clipboard.writeText("ut09.holy.gg:25898").then(() => {{
        const textSpan = document.getElementById('ip-text');
        const orig = textSpan.textContent;
        textSpan.textContent = "¡Copiado!";
        setTimeout(() => {{
          textSpan.textContent = orig;
        }}, 2000);
      }}).catch(err => {{
        alert("IP: ut09.holy.gg:25898");
      }});
    }}

    window.addEventListener('DOMContentLoaded', init);
  </script>
</body>
</html>
'''

    # Save to dist/index.html (for Cloudflare Pages deployment)
    os.makedirs('dist', exist_ok=True)
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Save to stats.html in root directory so user can open locally too!
    with open('stats.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Sitio web generado exitosamente en dist/index.html y stats.html!")

if __name__ == '__main__':
    generate_website()
