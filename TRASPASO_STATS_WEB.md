# TRASPASO: Página web de estadísticas del personaje (Stargolden)

**Fecha**: 27 de septiembre de 2026
**Carpeta de trabajo**: `C:\Users\amaro\OneDrive\Desktop\Bot para server`
**Tarea pendiente**: Generar una página web (`stats.html`) con TODAS las estadísticas del personaje **Stargolden** (UUID: `f0d03f69-7585-3e09-aaaa-cba59086d8db`) del servidor Minecraft.

---

## 1. QUÉ YA ESTÁ HECHO (no repetir)

### Datos descargados del servidor (ya están en la carpeta local)

| Archivo local | Contenido | Fuente en el servidor |
|---|---|---|
| `stargolden_stats.json` (13.7 KB) | Estadísticas vanilla de Minecraft (bloques minados, items usados, crafteos, muertes, kills, distancias, etc.) | `/world/players/stats/f0d03f69-7585-3e09-aaaa-cba59086d8db.json` |
| `stargolden_auraskills.yml` (701 B) | Habilidades de AuraSkills: niveles y XP de 11 skills (fishing, fighting, alchemy, farming, agility, excavation, foraging, archery, mining, defense, enchanting) + mana | `/plugins/AuraSkills/userdata/f0d03f69-7585-3e09-aaaa-cba59086d8db.yml` |
| `stargolden_advancements.json` (66 KB) | Logros/advancements (418 claves, incluye recetas desbloqueadas) | `/world/players/advancements/f0d03f69-7585-3e09-aaaa-cba59086d8db.json` |

### Estructura de los datos

**`stargolden_stats.json`**:
```json
{
  "stats": {
    "minecraft:mined": {"minecraft:torch": 5, "minecraft:cherry_log": 17, ...},
    "minecraft:used": {"minecraft:stone_axe": 64, ...},
    "minecraft:dropped": {...},
    "minecraft:crafted": {...},
    "minecraft:picked_up": {"minecraft:cobblestone": 4026, ...},
    "minecraft:custom": {"minecraft:play_time": 123456, "minecraft:deaths": 5, ...},
    "minecraft:killed_by": {"minecraft:zombie": 3, ...},
    "minecraft:broken": {...},
    "minecraft:killed": {"minecraft:skeleton": 43, ...}
  },
  "DataVersion": 4903
}
```
- Las distancias están en **centímetros** (`walk_one_cm` → dividir entre 100 para metros).
- `play_time` está en **ticks** (20 ticks = 1 segundo).
- Los nombres de items/mobs son IDs de Minecraft (ej. `minecraft:skeleton`).

**`stargolden_auraskills.yml`**:
```yaml
uuid: f0d03f69-7585-3e09-aaaa-cba59086d8db
skills:
  auraskills/fishing: {level: 0, xp: 0.0}
  auraskills/fighting: {level: 3, xp: 937.2}
  auraskills/alchemy: {level: 3, xp: 396.0}
  auraskills/farming: {level: 0, xp: 72.5}
  auraskills/agility: {level: 5, xp: 1165.15}
  auraskills/excavation: {level: 3, xp: 200.66}
  auraskills/foraging: {level: 2, xp: 178.82}
  auraskills/archery: {level: 0, xp: 97.0}
  auraskills/mining: {level: 4, xp: 71.2}
  auraskills/defense: {level: 4, xp: 442.29}
  auraskills/enchanting: {level: 0, xp: 0.0}
mana: 32.0
```

**`stargolden_advancements.json`**:
```json
{
  "minecraft:recipes/decorations/crafting_table": {
    "criteria": {"unlock_right_away": "2026-09-25 20:14:24 +0000"},
    "done": true
  },
  ...
}
```
- Cada clave es un advancement/receta. `"done": true` = completado.
- Para mostrar solo logros reales (no recetas), filtrar claves que NO empiecen con `minecraft:recipes/`.

---

## 2. QUÉ FALTA HACER

### Tarea principal
Crear `stats.html` — una página web bonita con tema Minecraft que muestre:

1. **Cabecera**: Avatar de Stargolden (se puede usar `https://mc-heads.net/avatar/f0d03f69-7585-3e09-aaaa-cba59086d8db` o `https://minotar.net/helm/f0d03f69-7585-3e09-aaaa-cba59086d8db/100.png`), nombre, UUID.
2. **Resumen general** (de `minecraft:custom`): tiempo jugado (formateado a h/m/s), muertes, mob kills, player kills, saltos, distancia caminada (km), distancia volada, etc.
3. **Habilidades AuraSkills**: tabla o barras de progreso con las 11 skills (nivel + XP + barra de progreso).
4. **Logros**: contador de logros completados (excluyendo `minecraft:recipes/`) y lista de los principales.
5. **Mobs asesinados** (de `minecraft:killed`): tabla con mob → cantidad.
6. **Bloques minados** (de `minecraft:mined`): top 10.
7. **Items crafteados** (de `minecraft:crafted`): top 10.
8. **Items recogidos** (de `minecraft:picked_up`): top 10.
9. **Muertes por causa** (de `minecraft:killed_by`): tabla.

### Requisitos de diseño
- Tema oscuro estilo Minecraft (verde `#3f8f3f` / `#55ff55`, fondo `#1a1a1a`, bordes pixelados).
- Todo el texto en **español**.
- Traducir los IDs de Minecraft a nombres legibles (ej. `minecraft:skeleton` → "Esqueleto", `minecraft:cobblestone` → "Roca").
- Un solo archivo HTML autocontenido (CSS inline, sin dependencias externas excepto el avatar).
- Responsive (que se vea bien en móvil).

### Formato de tiempo
- `play_time` (ticks): `ticks / 20 = segundos` → formatear como `Xh Ym Zs`.
- Distancias (cm): `cm / 100 = metros` → `X.XX km` si es grande.

---

## 3. CÓMO ACCEDER AL SERVIDOR (si se necesitan datos frescos)

Credenciales en `bot_config.json` (misma carpeta):
```json
{
  "panel_url": "https://panel.holy.gg",
  "api_key": "ptlc_...",
  "server_id": "4bd17cbb"
}
```

### API de Pterodactyl (client API)
```python
import requests
headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0"}

# Listar archivos
r = requests.get(f"{panel_url}/api/client/servers/{server_id}/files/list",
                 headers=headers, params={"directory": "/world/players/stats"}, timeout=15)

# Leer archivo
r = requests.get(f"{panel_url}/api/client/servers/{server_id}/files/contents",
                 headers=headers, params={"file": "/world/players/stats/f0d03f69-7585-3e09-aaaa-cba59086d8db.json"}, timeout=15)
```

### ADVERTENCIAS IMPORTANTES (aprendidas con errores)
1. **El daemon es inestable**: devuelve `500 DaemonConnectionException` intermitentemente. **Siempre** usar retry (3-4 intentos con `time.sleep(3)`).
2. **El User-Agent es OBLIGATORIO**: sin él, el panel devuelve HTML de login en vez de JSON.
3. **NO ejecutar comandos destructivos** en el servidor (clear, reset, delete) — el usuario ya perdió su inventario una vez por esto. Solo lectura.
4. **Encoding en Windows**: la consola usa cp1252. No imprimir caracteres como `✓` o `ñ` en prints de Python sin `# -*- coding: utf-8 -*-` o usar `print()` con texto ASCII. Para escribir archivos usar `encoding='utf-8'`.
5. **El archivo de stats se actualiza** cuando el jugador sale del juego o cada ~5 min. Si se quiere data fresca, re-descargar antes de generar.

---

## 4. ARCHIVOS ÚTILES EXISTENTES

| Archivo | Para qué sirve |
|---|---|
| `holy_bot_llm.py` | Bot LLM que controla el servidor (status, restart, comandos). No necesario para esta tarea. |
| `holy_files.py` | File manager vía API Pterodactyl (ls, cat, write). Útil como referencia de cómo llamar a la API. |
| `bot_config.json` | Credenciales del panel. |
| `stargolden_stats.json` | **Datos principales para la página.** |
| `stargolden_auraskills.yml` | Habilidades AuraSkills. |
| `stargolden_advancements.json` | Logros. |

---

## 5. PLAN SUGERIDO

1. Escribir `stats_web.py` (script Python compacto, < 300 líneas) que:
   - Lee los 3 archivos de datos locales.
   - Traduce IDs → nombres en español (diccionario pequeño para los más comunes + fallback que limpia el ID: `minecraft:skeleton` → "Skeleton").
   - Genera `stats.html` con f-strings o plantilla.
2. Ejecutar `python stats_web.py`.
3. Verificar abriendo `stats.html` en navegador (o `python -m http.server`).
4. Entregar al usuario la ruta del archivo.

**IMPORTANTE**: No intentar escribir el HTML dentro de un diccionario gigante de traducciones en un solo `file_write` — el archivo se trunca si es muy grande. Dividir en: (a) script generador pequeño, (b) diccionario de traducciones en archivo separado si hace falta, o (c) usar un diccionario mínimo y un fallback automático.

---

## 6. CONTACTO / CONTEXTO DEL USUARIO

- Usuario: **Stargolden** (dueño del servidor, habla español).
- Servidor: Holy Hosting, panel.holy.gg, server_id `4bd17cbb`.
- El usuario quiere ver "todas las estadísticas de mi personaje" en una página web.
- Prefiere que NO se toque nada más del servidor (solo lectura).
- Si algo falla, ser honesto y decir exactamente qué se verificó y qué no.
