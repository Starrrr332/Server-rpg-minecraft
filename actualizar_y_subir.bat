@echo off
cd /d "%~dp0"
title Actualizar Estadisticas y Publicar en Cloudflare
color 0b
echo ========================================================
echo   ACTUALIZAR ESTADISTICAS Y PUBLICAR EN VIVO
echo ========================================================
echo.
echo [1/4] Descargando ultimas estadisticas de Holy Hosting...
python sync_all_players.py
if %ERRORLEVEL% NEQ 0 (
    echo [!] Error al descargar datos.
    pause
    exit /b
)

echo.
echo [2/5] Compilando base de datos y leaderboards...
python build_database.py
if %ERRORLEVEL% NEQ 0 (
    echo [!] Error al procesar la base de datos.
    pause
    exit /b
)

echo.
echo [3/5] Sincronizando cuentas en la base de datos MySQL de Holy Hosting...
python sync_sql_accounts.py
if %ERRORLEVEL% NEQ 0 (
    echo [!] Error al sincronizar con MySQL.
    pause
    exit /b
)

echo.
echo [4/5] Generando aplicacion web optimizada...
python generate_web.py
if %ERRORLEVEL% NEQ 0 (
    echo [!] Error al generar el HTML.
    pause
    exit /b
)

echo.
echo [5/5] Subiendo cambios a GitHub y desplegando en Cloudflare...
"C:\Users\amaro\mingit\cmd\git.exe" add .
"C:\Users\amaro\mingit\cmd\git.exe" commit -m "chore(stats): actualizacion automatica de estadisticas de jugadores"
"C:\Users\amaro\mingit\cmd\git.exe" push origin main

echo.
echo ========================================================
echo   EXITO: Cambios enviados a GitHub!
echo   Cloudflare Pages detectara los cambios y actualizara
echo   tu pagina web publica en aproximadamente 10 segundos.
echo ========================================================
pause
