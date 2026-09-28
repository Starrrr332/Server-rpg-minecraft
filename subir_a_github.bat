@echo off
title Subir Proyecto a GitHub
color 0a
echo ========================================================
echo               SUBIR PROYECTO A GITHUB
echo ========================================================
echo.
echo Asegurate de haber creado un repositorio vacio en https://github.com/new
echo.
set /p REPO_URL="Pega aqui la URL de tu repositorio (ej: https://github.com/usuario/mi-servidor.git): "

if "%REPO_URL%"=="" (
    echo [!] No ingresaste ninguna URL. Operacion cancelada.
    pause
    exit /b
)

echo.
echo [1/3] Configurando repositorio remoto...
"C:\Users\amaro\mingit\cmd\git.exe" remote remove origin 2>nul
"C:\Users\amaro\mingit\cmd\git.exe" remote add origin %REPO_URL%

echo [2/3] Verificando rama principal...
"C:\Users\amaro\mingit\cmd\git.exe" branch -M main

echo [3/3] Subiendo archivos a GitHub...
"C:\Users\amaro\mingit\cmd\git.exe" push -u origin main

echo.
echo ========================================================
echo Proceso finalizado. Si aparecio una ventana pidiendo usuario/token, autorizalo.
echo ========================================================
pause
