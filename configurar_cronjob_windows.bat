@echo off
cd /d "%~dp0"
title Configurar Cronjob Automatico de Estadisticas y MySQL
color 0a
echo ========================================================
echo       CONFIGURAR CRONJOB AUTOMATICO (CADA 30 MINUTOS)
echo ========================================================
echo.
echo Esta tarea programara la ejecucion automatica de la sincronizacion:
echo 1. Descarga datos de Holy Hosting
echo 2. Actualiza la base de datos MySQL (cuentas de jugadores)
echo 3. Actualiza y publica la web en Cloudflare
echo.

set SCRIPT_PATH=%~dp0actualizar_y_subir.bat

echo Registrando tarea programada en Windows (schtasks)...
schtasks /create /tn "HolyServer_StatsSync" /tr "\"%SCRIPT_PATH%\"" /sc minute /mo 30 /f

echo.
if %ERRORLEVEL% EQU 0 (
    echo [EXITO] Cronjob configurado correctamente en Windows!
    echo Se ejecutara automaticamente cada 30 minutos.
) else (
    echo [!] Hubo un detalle al crear la tarea. Si es necesario, ejecuta este archivo como Administrador.
)
echo.
pause
