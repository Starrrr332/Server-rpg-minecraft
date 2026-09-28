# -*- coding: utf-8 -*-
"""
Script todo-en-uno para el servidor:
1. Descarga las estadísticas actualizadas de todos los jugadores desde Holy Hosting.
2. Procesa los datos, calcula leaderboards y traduce todos los IDs de Minecraft.
3. Genera la página web profesional en stats.html y dist/index.html.
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
    print("Iniciando actualizacion completa de estadisticas...")
    
    if not run_step("Paso 1: Sincronizar datos de jugadores desde el servidor", [sys.executable, "sync_all_players.py"]):
        return
        
    if not run_step("Paso 2: Compilar base de datos y leaderboards", [sys.executable, "build_database.py"]):
        return
        
    if not run_step("Paso 3: Generar sitio web profesional (dist/ e index.html)", [sys.executable, "generate_web.py"]):
        return

    print("\n" + "="*50)
    print("[EXITO] La pagina web esta lista y 100% actualizada.")
    print("Puedes abrir 'stats.html' directamente en tu navegador")
    print("O desplegar la carpeta 'dist/' a Cloudflare Pages.")
    print("="*50 + "\n")

if __name__ == '__main__':
    main()
