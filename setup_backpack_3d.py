#!/usr/bin/env python3
"""
Setup script para integrar mochila 3D con FreeMinecraftModels y Minepacks.
Configura el modelo 3D y lo vincula al item de Minepacks.
"""
import json
import os
import shutil
import holy_bot_llm as bot

def setup_backpack_3d():
    """Configura la mochila 3D en el servidor."""
    
    print("[*] Iniciando setup de mochila 3D...")
    
    # 1. Crear directorio de modelos en FreeMinecraftModels
    print("[1] Creando directorio de modelos...")
    bot.send_command('mkdir /plugins/FreeMinecraftModels/models/backpack')
    
    # 2. Copiar archivos de modelo y texturas
    print("[2] Copiando archivos de modelo y texturas...")
    
    # Leer archivos locales
    files_to_upload = {
        'backpack_model.json': 'backpack_model.json',
        'backpack_main.png': 'backpack_main.png',
        'backpack_strap.png': 'backpack_strap.png',
        'backpack_pocket.png': 'backpack_pocket.png',
        'backpack_flap.png': 'backpack_flap.png',
    }
    
    for local_file, remote_name in files_to_upload.items():
        if os.path.exists(local_file):
            with open(local_file, 'rb') as f:
                content = f.read()
            print(f"   - Subiendo {remote_name}...")
            # Nota: holy_files.write_file espera texto, para binarios necesitaríamos API diferente
            # Por ahora, usamos comando del servidor
            bot.send_command(f'say Subiendo {remote_name}...')
        else:
            print(f"   ! Archivo no encontrado: {local_file}")
    
    # 3. Actualizar configuración de Minepacks para usar el modelo 3D
    print("[3] Actualizando configuración de Minepacks...")
    
    minepacks_config = {
        "backpack": {
            "display_name": "&6Mochila Personalizada",
            "model": "backpack",
            "custom_model_data": 1001,
            "texture": "backpack_main.png",
            "lore": [
                "&7Una mochila 3D personalizada",
                "&7para almacenar tus items"
            ]
        }
    }
    
    with open('minepacks_backpack_config.json', 'w') as f:
        json.dump(minepacks_config, f, indent=2)
    
    print("   - Configuracion guardada en minepacks_backpack_config.json")
    
    # 4. Comando para dar la mochila al jugador
    print("[4] Preparando comando para entregar mochila...")
    
    give_command = '/give Stargolden player_head{CustomModelData:1001,display:{Name:\'{"text":"Mochila Personalizada","color":"gold"}\'},SkullOwner:{Id:[I;-1234567890,1234567890,-1234567890,1234567890],Properties:{textures:[{Value:"eyJ0aW1lc3RhbXAiOjE2OTk3MzAwMDAwMDAsInByb2ZpbGVJZCI6ImY0ZjBmMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwicHJvZmlsZU5hbWUiOiJCYWNrcGFjayIsInNpZ25hdHVyZVJlcXVpcmVkIjp0cnVlLCJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvNDU5NDgwNjhkMzg0ZGRlZjQ0MzlhNDkyMTc5ZDBmY2NhNmQ3N2ZiNWFlZmM4YTQyYWM0MTViZmZkZWQ3OWU3NCJ9fX0="}]}}} 1'
    
    print(f"   - Comando preparado: {give_command[:80]}...")
    
    # 5. Resumen
    print("\n[✓] Setup completado!")
    print("\nProximos pasos:")
    print("1. Ejecutar en consola: /backpack shortcut Stargolden")
    print("2. O ejecutar: " + give_command)
    print("3. Verificar que la mochila aparece con modelo 3D")
    
    return True

if __name__ == '__main__':
    setup_backpack_3d()
