# ☁️ Guía de Configuración: Copias de Seguridad Automáticas en Google Drive

El sistema **Holy Server Sentinel** incluye integración directa para crear copias de seguridad comprimidas en el servidor (`world`, `plugins`, configuraciones críticas) y subirlas automáticamente a tu **Google Drive** en una carpeta llamada `HolyServer_Backups`.

---

## 🚀 Método Recomendado: Conexión OAuth2 (Cuenta Personal o Institucional)

### Paso 1: Obtener `credentials.json` desde Google Cloud Console
1. Ingresa a la [Consola de Google Cloud](https://console.cloud.google.com/).
2. Crea un proyecto (o selecciona uno existente, por ejemplo `HolyServer`).
3. Ve a **APIs & Services (APIs y servicios)** > **Library (Biblioteca)**.
4. Busca **Google Drive API** y haz clic en **Enable (Habilitar)**.
5. Ve a **APIs & Services** > **OAuth consent screen (Pantalla de consentimiento OAuth)**:
   * Tipo de usuario: **External (Externo)**.
   * Nombre de app: `HolyServer Backup`.
   * Correo electrónico de soporte: tu correo.
   * En la sección de **Test Users (Usuarios de prueba)**, añade tu correo de Google/Gmail.
6. Ve a **APIs & Services** > **Credentials (Credenciales)**:
   * Haz clic en **Create Credentials (Crear credenciales)** > **OAuth Client ID**.
   * Tipo de aplicación: **Desktop App (Aplicación de escritorio)**.
   * Nombre: `HolyServer Backup Client`.
   * Haz clic en **Create**.
7. En la ventana emergente, haz clic en **Download JSON (Descargar JSON)**.
8. Renombra el archivo descargado a:
   👉 `credentials.json`
9. Pega este archivo en la carpeta principal del bot:
   `c:\Users\amaro\OneDrive\Desktop\Bot para server\credentials.json`

---

### Paso 2: Autorizar la Primera Subida
Una vez colocado `credentials.json`, ejecuta en tu terminal:
```bash
python google_drive_manager.py
```
Se abrirá automáticamente una pestaña en tu navegador solicitándote iniciar sesión con tu cuenta de Google y autorizar el acceso para guardar copias. 
* Tras autorizar, se generará automáticamente el archivo `token.json` y el sistema no volverá a pedir inicio de sesión nunca más.

---

## 🛡️ ¿Cómo Funciona la Copia de Seguridad?
Puedes activar una copia de seguridad inmediata en cualquier momento ejecutando:
```bash
python server_sentinel.py --backup
```
1. El centinela ejecuta `/save-all` para consolidar datos de jugadores y mundos.
2. Comprime las carpetas `world`, `plugins`, `server.properties`, `bukkit.yml` y `spigot.yml` directamente en el host (sin saturar tu ancho de banda local).
3. Descarga el paquete a `backups/HolyServer_Backup_YYYYMMDD_HHMMSS.tar.gz`.
4. Elimina el archivo temporal del host para no consumir el disco del servidor.
5. Sube la copia a la carpeta `HolyServer_Backups` en tu Google Drive.
6. **Rotación Automática:** Mantiene siempre las 5 copias más recientes en Google Drive, eliminando las más antiguas automáticamente para ahorrar almacenamiento.

---

## 📊 Mando de Control y Monitoreo de Memoria
Para ver el estado en tiempo real de RAM y CPU:
```bash
python server_sentinel.py --status
```
Para ejecutar un ciclo de monitoreo continuo en segundo plano:
```bash
python server_sentinel.py --monitor
```
Para ejecutar una limpieza suave preventiva de memoria (sin reiniciar el servidor):
```bash
python server_sentinel.py --clean
```
