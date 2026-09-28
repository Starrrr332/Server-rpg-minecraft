# Guía Definitiva: Alojamiento Gratuito en Cloudflare Pages 🚀

Esta plataforma web de estadísticas de Minecraft ha sido diseñada específicamente para **Cloudflare Pages**, el mejor servicio de hosting estático del mundo, 100% gratuito, con ancho de banda ilimitado, protección contra ataques DDoS y certificado SSL automático (`https://`).

---

## 🌟 Opciones para Alojar tu Página (Elige la que prefieras)

### Opción 1: Subida Directa en la Web (Sin instalar nada, 1 Minuto) ⚡ *(Recomendada)*

1. Entra a [dash.cloudflare.com](https://dash.cloudflare.com/) e inicia sesión con tu cuenta gratuita de Cloudflare (o regístrate si no tienes una).
2. En el menú de la izquierda, ve a **Compute (Workers) > Workers y Pages**.
3. Haz clic en el botón azul **Crear aplicación** (Create application).
4. Selecciona la pestaña **Pages** y haz clic en **Cargar recursos** (Upload assets).
5. Escribe el nombre que quieras para tu proyecto (por ejemplo: `holy-server-rpg` o `stargolden-server`).
6. Arrastra y suelta la carpeta `dist` (o el archivo comprimido `dist.zip` que ya te dejamos listo en la carpeta).
7. Haz clic en **Implementar sitio** (Deploy site).
8. **¡Listo!** En 5 segundos tendrás tu enlace público mundial activo:  
   👉 `https://tu-nombre-de-proyecto.pages.dev`

---

### Opción 2: Despliegue desde tu Computadora con 1 Doble Clic 💻

En tu carpeta de trabajo hemos dejado el archivo ejecutable:
👉 `desplegar_cloudflare.bat`

1. Haz doble clic en `desplegar_cloudflare.bat`.
2. Se abrirá una ventana que te pedirá iniciar sesión en Cloudflare en tu navegador (solo la primera vez).
3. Una vez autorizado, subirá automáticamente la carpeta `dist` y te devolverá tu URL oficial en vivo.

---

### Opción 3: Despliegue mediante Terminal con Wrangler CLI 🛠️

Si prefieres usar la consola o tienes un token de Cloudflare:

```powershell
# 1. Iniciar sesión en Cloudflare
npx wrangler login

# 2. Desplegar la carpeta dist a Cloudflare Pages
npx wrangler pages deploy dist --project-name holy-server-stats
```

---

## 🔄 ¿Cómo Actualizar las Estadísticas en el Futuro?

Cada vez que quieras refrescar las estadísticas con los nuevos datos del servidor:

1. Ejecuta en tu terminal:
   ```powershell
   python update_stats.py
   ```
   *Este comando descarga automáticamente los datos frescos de todos los jugadores desde Holy Hosting, recalcula clasificaciones y actualiza la web.*

2. Vuelve a subir la carpeta `dist` o ejecuta `desplegar_cloudflare.bat`.
