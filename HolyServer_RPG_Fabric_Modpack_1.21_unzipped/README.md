# ⚔️ Holy RPG - Modpack Client-Side Fabric (MC 1.21.x / 26.2)

> **Modpack 100% Client-Side diseñado para transformar Minecraft en una experiencia RPG inmersiva de última generación, con la mejor interfaz gráfica (HUD), animaciones fluidas, sonido atmosférico 3D y rendimiento optimizado.**
> 
> ✅ **100% Compatible con Servidores Multijugador Vanilla y Paper/Spigot**: No requiere que el servidor instale ningún mod. No interfiere con anti-cheats (incluye minimapa versión Fair-Play sin radares ilegales).

---

## 🌟 Características Principales

### 1. 🛡️ Interfaz de Usuario & HUD RPG
* **RPG-HUD**: Reemplaza por completo el HUD plano original por una barra curva de vitalidad y resistencia/maná estilo MMORPG. Incluye indicador de durabilidad de armadura en tiempo real, widgets flotantes de efectos de pociones con temporizadores circulares y brújula de orientación en el borde superior.
* **Provi's Health Bars**: Barras de vida flotantes encima de todos los mobs y jugadores, con colores diferenciados para Jefes de Élite, visualización numérica de daño por golpe recibido y estados alterados.
* **Equipment Compare**: Al pasar el cursor sobre un arma o armadura presionando `Shift`, despliega un menú comparativo lado a lado con tu equipamiento actual (ejemplo: `+4.5 Daño de Ataque [Verde]`, `-1 Armadura [Rojo]`), idéntico a Diablo IV y World of Warcraft.
* **Dynamic Crosshair**: La mira central reacciona al entorno: se convierte en espada al apuntar a enemigos, en mano o cofre al interactuar con cofres/puertas, y se desvanece suavemente al explorar el paisaje.
* **AppleSkin**: Revela la saturación oculta de todos los alimentos, el agotamiento acumulado y cuánta vida restaurará cada comida antes de consumirla.
* **ShulkerBoxTooltip**: Ventana emergente con vista gráfica en miniatura del contenido de cajas de shulker y mochilas al pasar el cursor sobre ellas.
* **Mandala's GUI - Dark Mode (Resource Pack incluido)**: Rediseña todos los menús, cofres, mesas de crafteo y ventanas del juego con temática de fantasía oscura y marcos dorados RPG.

### 2. 🗺️ Navegación & Cartografía Fair-Play
* **Xaero's Minimap (Fair-Play Edition)**: Minimapa circular/cuadrado personalizable de alta resolución. Permite marcar puntos de ruta (Waypoints) para tu casa, la sede del Gremio de Aventureros, mazmorras y tu punto de muerte exacto.
* **Xaero's World Map**: Mapa de mundo completo en pantalla panorámica accesible con la tecla `M`, con exploración por cuadrícula, biomas y coordenadas precisas.

### 3. 🎬 Inmersión, Animaciones & Atmósfera
* **Traveler's Titles**: Muestra un título cinemático en pantalla estilo *Elden Ring / Dark Souls* al ingresar a un nuevo bioma o región descubierta.
* **Not Enough Animations**: Animaciones realistas en 1ra y 3ra persona: comer, beber pociones, remar, escalar escaleras, gatear y posición de defensa con escudo.
* **3D Skin Layers**: Modela la segunda capa de la skin en 3D con volumen y relieve real.
* **Wavey Capes**: Físicas de oleaje suave y viento realista para las capas.
* **LambDynamicLights**: Iluminación dinámica en tiempo real: antorchas, linternas y armas mágicas iluminan la cueva mientras las sostienes en la mano o en la zurda.

### 4. 🔊 Sonido Acústico & Espacial
* **Sound Physics Remastered**: Motor de reverberación y acústica física: eco real en cavernas profundas, absorción sonora a través de muros de piedra y atenuación bajo el agua.
* **Presence Footsteps**: Sonidos de pisadas acústicas diferenciadas por cada bloque del juego (madera crujiente, piedra resonante, nieve esponjosa, fango).

### 5. ⚡ Motor de Rendimiento Gráfico & Shaders
* **Sodium**: Motor de renderizado moderno que triplica los fotogramas por segundo (FPS) y estabiliza el frametime.
* **Iris Shaders**: Soporte para shaders de gama alta (Complementary Reimagined, BSL, Bliss) a máximos FPS.
* **ImmediatelyFast**: Optimiza el renderizado de la interfaz, textos, inventarios y HUD para pantallas de 144Hz/240Hz.
* **FerriteCore**: Reduce drásticamente el consumo de memoria RAM del cliente hasta en un 50%.
* **Inventory Profiles Next**: Ordena inventarios y cofres con un solo clic con atajos inteligentes.

---

## ⌨️ Guía de Atajos de Teclado (Hotkeys)

| Tecla | Acción | Mod |
| :--- | :--- | :--- |
| `M` | Abrir / Cerrar Mapa Mundial en pantalla completa | Xaero's World Map |
| `B` | Crear nuevo Waypoint (Punto de ruta) en tu ubicación | Xaero's Minimap |
| `U` | Ver lista y gestionar todos tus Waypoints guardados | Xaero's Minimap |
| `Y` | Configuración del Minimapa | Xaero's Minimap |
| `Shift` (Hover) | Comparar estadísticas del ítem con el equipo puesto | Equipment Compare |
| `R` | Ordenar inventario / cofre actual | Inventory Profiles Next |
| `O` | Shaders y ajustes gráficos avanzados | Iris / Sodium |
| `K` | Configuración de animaciones | Not Enough Animations |
| `P` | Configuración de sonido y física acústica | Sound Physics |
| `Esc` > `Mods` | Menú interactivo de configuración de todos los mods | Mod Menu |

---

## 📦 Guía de Instalación Paso a Paso

### Método 1: Prism Launcher / Modrinth App (Recomendado)
1. Abre tu launcher (**Prism Launcher** o **Modrinth App**).
2. Haz clic en **Añadir Instancia** (Add Instance).
3. Selecciona:
   * **Versión de Minecraft**: `1.21.1` (o 1.21).
   * **Modloader**: `Fabric` (última versión estable recomendada).
4. Abre la carpeta de la instancia (haz clic en *Folder* o *Ver Carpeta*).
5. Copia el contenido de este modpack:
   * Pega la carpeta `mods/` dentro de la carpeta de la instancia.
   * Pega la carpeta `config/` dentro de la carpeta de la instancia.
   * Pega la carpeta `resourcepacks/` dentro de la carpeta de la instancia.
6. Inicia el juego.
7. En el menú de inicio, ve a `Opciones` > `Paquetes de recursos` y activa **Mandala's GUI - Dark Mode**.

---

### Método 2: Launcher Oficial de Minecraft
1. Descarga e instala **Fabric Loader para Minecraft 1.21.1** desde [fabricmc.net](https://fabricmc.net/use/installer/).
2. Presiona `Windows + R`, escribe `%appdata%\.minecraft` y presiona Enter.
3. Si no existe, crea una carpeta llamada `mods`.
4. Copia todos los archivos `.jar` de la carpeta `modpack_rpg_client/mods/` dentro de tu carpeta `%appdata%\.minecraft\mods\`.
5. Copia los archivos de `modpack_rpg_client/config/` a `%appdata%\.minecraft\config\`.
6. Copia `modpack_rpg_client/resourcepacks/MandalasGUI_DarkMode_1.21.zip` a `%appdata%\.minecraft\resourcepacks\`.
7. Abre el launcher oficial de Minecraft, selecciona el perfil **Fabric Loader 1.21.1** y presiona **Jugar**.
8. Activa el paquete de recursos de interfaz oscura en `Opciones > Paquetes de recursos`.

---

## 🎨 Recomendación de Shaders (Opcional)
Gracias a la inclusión de **Sodium + Iris**, puedes instalar shaders sin pérdida de rendimiento. Shaders recomendados para temática RPG Medieval:
1. **Complementary Reimagined**: Estilo RPG fantasía con neblina volumétrica y auroras boreales.
2. **BSL Shaders**: Colores cálidos medievales y reflejos de agua hiperrealistas.

*Para instalar un shader: Descarga el archivo `.zip` del shader y arrástralo directamente a la ventana de `Opciones > Shaders`.*
