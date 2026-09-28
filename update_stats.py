# -*- coding: utf-8 -*-
"""
Script todo-en-uno para el servidor:
1. Descarga las estadísticas actualizadas de todos los jugadores desde Holy Hosting.
2. Procesa los datos, calcula leaderboards y traduce todos los IDs de Minecraft.
3. Sincroniza y actualiza las cuentas de jugadores en la base de datos MySQL de Holy Hosting.
4. Genera la página web profesional en stats.html y dist/index.html.
"""
import subprocess
import sys
import os

def run_step(description, command):
    print(f"\n==========================================")
    print(f">> {description}")
    print(f"==========================================")
    res = subprocess.run(command, shell=True)
    if res.returncode != 0:
        print(f"[!] Error ejecutando: {command}")
        return False
    return True

def main():
    print("Iniciando actualizacion completa (Stats + MySQL + Web)...")
    
    if not run_step("Paso 1: Sincronizar datos de jugadores desde Holy Hosting", [sys.executable, "sync_all_players.py"]):
        return
        
    if not run_step("Paso 2: Compilar base de datos local y leaderboards", [sys.executable, "build_database.py"]):
        return

    if not run_step("Paso 3: Sincronizar cuentas vinculadas en MySQL del Hosting", [sys.executable, "sync_sql_accounts.py"]):
        return
        
    if not run_step("Paso 4: Generar sitio web profesional (dist/ e index.html)", [sys.executable, "generate_web.py"]):
        return

    print("\n" + "="*50)
    print("[EXITO] Proceso finalizado.")
    print("- Base de datos MySQL de Holy Hosting actualizada.")
    print("- Web en stats.html y dist/index.html actualizada.")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
