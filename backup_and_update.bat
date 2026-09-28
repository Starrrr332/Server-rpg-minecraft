@echo off
rem =============================================
rem Backup and mass update script for Minecraft server
rem =============================================

set "SERVER_ROOT=C:\Users\amaro\OneDrive\Desktop\Bot para server"
set "BACKUP_ROOT=%SERVER_ROOT%\backups"

rem Get current date in yyyy-MM-dd format using PowerShell
for /f "usebackq tokens=*" %%d in (`powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd'"`) do set "CUR_DATE=%%d"

rem Create backup folder for today
set "TODAY_BACKUP=%BACKUP_ROOT%\backup_%CUR_DATE%"
if not exist "%TODAY_BACKUP%" (
    mkdir "%TODAY_BACKUP%"
)

rem ---------------------------------------------------------------------
rem 1) Create a zip of the entire server folder (excluding the backups folder)
rem ---------------------------------------------------------------------
rem Use PowerShell's Compress-Archive. Exclude the backups folder to avoid recursion.
powershell -NoProfile -Command "Compress-Archive -Path '%SERVER_ROOT%\*' -DestinationPath '%TODAY_BACKUP%\server_%CUR_DATE%.zip' -Force -Exclude 'backups'"

if %ERRORLEVEL% neq 0 (
    echo Error during compression. Exiting.
    exit /b 1
)

rem ---------------------------------------------------------------------
rem 2) Dump MySQL guild_stats table
rem ---------------------------------------------------------------------
rem Ensure mysqldump is in PATH or provide full path to it.
set "MYSQL_HOST=38.97.61.71"
set "MYSQL_PORT=3306"
set "MYSQL_USER=u63121_YEHsFXzBrp"
set "MYSQL_PASSWORD=U^TN^^AotPQeST0hg+Vc0KfF"
set "MYSQL_DATABASE=s63121_mc_accounts"

mysqldump -h %MYSQL_HOST% -P %MYSQL_PORT% -u %MYSQL_USER% -p%MYSQL_PASSWORD% %MYSQL_DATABASE% guild_stats > "%TODAY_BACKUP%\guild_stats_%CUR_DATE%.sql"

if %ERRORLEVEL% neq 0 (
    echo MySQL dump failed. Exiting.
    exit /b 1
)

rem ---------------------------------------------------------------------
rem 3) Build all plugins using Maven
rem ---------------------------------------------------------------------
set "MODULE_ROOT=%SERVER_ROOT%\MinecraftPlugins"
pushd "%MODULE_ROOT%"
mvn clean package -DskipTests
if %ERRORLEVEL% neq 0 (
    echo Maven build failed. Exiting.
    popd
    exit /b 1
)
popd

rem ---------------------------------------------------------------------
rem 4) Copy compiled plugin JARs to the server plugins directory
rem ---------------------------------------------------------------------
set "PLUGIN_DIR=%SERVER_ROOT%\plugins"
if not exist "%PLUGIN_DIR%" mkdir "%PLUGIN_DIR%"

copy "%MODULE_ROOT%\backpack\target\backpack-1.0.0.jar" "%PLUGIN_DIR%" /Y
copy "%MODULE_ROOT%\directloot\target\directloot-1.0.0.jar" "%PLUGIN_DIR%" /Y
copy "%MODULE_ROOT%\shopenhancer\target\shopenhancer-1.0.0.jar" "%PLUGIN_DIR%" /Y
copy "%MODULE_ROOT%\mobdiff\target\mobdiff-1.0.0.jar" "%PLUGIN_DIR%" /Y

rem ---------------------------------------------------------------------
rem 5) Restart the server using holy_bot (already configured in bot_config.json)
rem ---------------------------------------------------------------------
python "%SERVER_ROOT%\holy_bot.py" restart

rem End of script
exit /b 0
