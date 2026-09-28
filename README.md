# ⚔️ Holy Server RPG - Estadísticas & Leaderboards

Dashboard web profesional de estadísticas y clasificaciones en tiempo real para servidores de Minecraft con **AuraSkills**, mapas 3D interactivos (**BlueMap**) y soporte multiplataforma (Java & Bedrock via Geyser).

Diseñado para ser alojado de forma 100% gratuita y ultrarrápida en **Cloudflare Pages**.

---

## 🌟 Características

- 🏆 **Tabla de Clasificación (Leaderboards)**:
  - Podio Top 3 con medallas (Oro 👑, Plata 🥈, Bronce 🥉) y avatares 3D.
  - Filtros por AuraSkills RPG, Tiempo Jugado, Mobs Asesinados, PvP Kills, Bloques Minados, Crafteos, Distancia Explorada y K/D Ratio.
- 👤 **Perfiles de Jugador Detallados**:
  - 11 Habilidades de AuraSkills (Pesca, Combate, Alquimia, Agricultura, Agilidad, Excavación, Tala, Tiro con arco, Minería, Defensa, Encantamiento).
  - Barras de progreso porcentual de nivel, XP y maná.
  - Top bloques minados e items crafteados con nombres en español.
  - Desglose de exploración (caminando, corriendo, en bote, a caballo).
  - Criaturas hostiles eliminadas y causas de muerte.
- 🗺️ **Mapa en Vivo (BlueMap)**:
  - Integración responsive del visor isométrico 3D en tiempo real del servidor.
- 🌐 **Soporte Multiplataforma**:
  - Compatible con jugadores de Minecraft Java Edition y Bedrock Edition (`.nombre`).
- ⚡ **Despliegue Gratuito en Cloudflare Pages**:
  - Listo para desplegar en 1 clic con CDN global, SSL automático y ancho de banda ilimitado.

---

## 🚀 Despliegue en Cloudflare Pages

### Método 1: Arrastrar y Soltar en el Dashboard (1 Minuto)
1. Ve a [dash.cloudflare.com](https://dash.cloudflare.com/).
2. Entra en **Workers y Pages** > **Crear aplicación** > **Pages** > **Cargar recursos**.
3. Sube la carpeta `dist/` o el archivo `dist.zip`.
4. ¡Listo! Tu web estará online en `https://tu-proyecto.pages.dev`.

### Método 2: Despliegue con Wrangler CLI
```bash
npx wrangler login
npx wrangler pages deploy dist --project-name holy-server-stats
```

---

## 🔄 Actualización de Estadísticas

Para sincronizar los datos más recientes del servidor y regenerar la web:

```bash
python update_stats.py
```

---

## 📂 Estructura del Proyecto

- `dist/index.html`: Aplicación web lista para producción.
- `stats.html`: Versión local de la página (abrible directamente en cualquier navegador).
- `sync_all_players.py`: Descarga segura de estadísticas vía API de Holy Hosting.
- `build_database.py`: Compilación de leaderboards y traducción de IDs de Minecraft.
- `generate_web.py`: Generador de la interfaz web.
- `bot_config.example.json`: Plantilla para credenciales de la API de Pterodactyl.

---
*Holy Server RPG © 2026. Creado para la comunidad.*
"# Server-rpg-minecraft" 
