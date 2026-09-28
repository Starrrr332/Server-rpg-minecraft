@echo off
title Desplegar Servidor RPG a Cloudflare Pages
color 0b
echo ========================================================
echo       DESPLEGAR ESTADISTICAS A CLOUDFLARE PAGES
echo ========================================================
echo.
echo Paso 1: Autenticar en Cloudflare (se abrira tu navegador si no has iniciado sesion)...
call cmd /c "npx wrangler login"

echo.
echo Paso 2: Desplegando carpeta dist/ a Cloudflare Pages...
call cmd /c "npx wrangler pages deploy dist --project-name holy-server-stats"

echo.
echo ========================================================
echo Si el despliegue finalizo, tu pagina ya esta en vivo en Cloudflare!
echo ========================================================
pause
