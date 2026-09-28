# -*- coding: utf-8 -*-
"""
Script de Verificación y Validación Rigurosa de Sintaxis YAML y Coherencia RPG.
Inspecciona recursivamente gremio_aventureros_lab/
"""

import os
import sys
import yaml

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

LAB_DIR = r"c:\Users\amaro\OneDrive\Desktop\Bot para server\gremio_aventureros_lab"

def main():
    print("=" * 70)
    print("  VERIFICACIÓN RIGUROSA DE ARCHIVOS YAML Y REFERENCIAS RPG")
    print(f"  Directorio: {LAB_DIR}")
    print("=" * 70)

    total_files = 0
    passed_files = 0
    failed_files = []
    parsed_yamls = {}

    # 1. Validación de Sintaxis YAML
    for root, dirs, files in os.walk(LAB_DIR):
        for f in files:
            if f.endswith('.yml') or f.endswith('.yaml'):
                total_files += 1
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, LAB_DIR)
                try:
                    with open(full_path, 'r', encoding='utf-8') as stream:
                        content = yaml.safe_load(stream)
                        parsed_yamls[rel_path] = content
                        passed_files += 1
                except Exception as e:
                    failed_files.append((rel_path, str(e)))

    print(f"\n[1/3] Sintaxis YAML: {passed_files}/{total_files} archivos válidos.")
    if failed_files:
        print("\n[!] ERRORES ENCONTRADOS EN SINTAXIS:")
        for rf, err in failed_files:
            print(f"  ❌ {rf}: {err}")
        sys.exit(1)
    else:
        print("  ✅ CERO errores de sintaxis en todos los archivos YAML.")

    # 2. Validación de Referencias Cruzadas (Quests -> Bosses & Items)
    print("\n[2/3] Verificación de Referencias Cruzadas (Integridad Referencial)...")
    quests_dir = os.path.join(LAB_DIR, 'customquests')
    bosses_dir = os.path.join(LAB_DIR, 'custombosses')
    items_dir = os.path.join(LAB_DIR, 'customitems')

    existing_bosses = set(os.listdir(bosses_dir)) if os.path.exists(bosses_dir) else set()
    existing_items = set(os.listdir(items_dir)) if os.path.exists(items_dir) else set()
    existing_quests = set(os.listdir(quests_dir)) if os.path.exists(quests_dir) else set()

    ref_warnings = []

    # Validar quests
    for q_file in existing_quests:
        q_path = os.path.join(quests_dir, q_file)
        with open(q_path, 'r', encoding='utf-8') as stream:
            data = yaml.safe_load(stream)
            if not isinstance(data, dict):
                continue
            
            # Revisar objetivos KILL_CUSTOM
            objs = data.get('customObjectives', {})
            if isinstance(objs, dict):
                for obj_id, obj_data in objs.items():
                    if isinstance(obj_data, dict) and obj_data.get('objectiveType') == 'KILL_CUSTOM':
                        target_boss = obj_data.get('filename')
                        if target_boss and target_boss not in existing_bosses:
                            ref_warnings.append(f"Misión '{q_file}' requiere el jefe '{target_boss}' que no está en custombosses/")

            # Revisar recompensas de items
            rewards = data.get('customRewards', [])
            if isinstance(rewards, list):
                for rew in rewards:
                    if 'filename=' in rew:
                        for part in rew.split(':'):
                            if part.startswith('filename='):
                                item_fn = part.split('=')[1]
                                # Ignorar items vanilla/preconstruidos de elitemobs como elite_scrap_* o ag_adventurer_*
                                if not (item_fn.startswith('elite_scrap_') or item_fn.startswith('ag_adventurer_')):
                                    if item_fn not in existing_items:
                                        ref_warnings.append(f"Misión '{q_file}' otorga el item '{item_fn}' no encontrado en customitems/")

    # Validar bosses loot list
    for b_file in existing_bosses:
        b_path = os.path.join(bosses_dir, b_file)
        with open(b_path, 'r', encoding='utf-8') as stream:
            data = yaml.safe_load(stream)
            if isinstance(data, dict):
                loot_list = data.get('uniqueLootList', [])
                for entry in loot_list:
                    item_file = entry.split(':')[0]
                    if item_file not in existing_items:
                        ref_warnings.append(f"Jefe '{b_file}' lista loot '{item_file}' no encontrado en customitems/")

    # Validar que Kaelen tenga todas las misiones registradas y existentes
    kaelen_path = os.path.join(LAB_DIR, 'npcs', 'maestro_cacerias_guild.yml')
    if os.path.exists(kaelen_path):
        with open(kaelen_path, 'r', encoding='utf-8') as stream:
            kd = yaml.safe_load(stream)
            for qn in kd.get('questFileName', []):
                if qn not in existing_quests:
                    ref_warnings.append(f"NPC Kaelen asigna la misión '{qn}' que no existe en customquests/")

    if ref_warnings:
        print("  ⚠️ Advertencias de referencia encontradas:")
        for w in ref_warnings:
            print(f"    - {w}")
    else:
        print("  ✅ Todas las referencias cruzadas (Quests -> Bosses -> Loot -> NPCs) son 100% COHERENTES.")

    # 3. Resumen de Contenidos Creados
    print("\n[3/3] Resumen de Activos en el Laboratorio:")
    print(f"  • Misiones Personalizadas (customquests/): {len(existing_quests)}")
    print(f"  • Jefes de Élite (custombosses/):           {len(existing_bosses)}")
    print(f"  • Armas, Armaduras e Ítems (customitems/): {len(existing_items)}")
    print(f"  • NPCs Configurados (npcs/):               {len(os.listdir(os.path.join(LAB_DIR, 'npcs')))}")
    print("=" * 70)
    print("  RESULTADO FINAL: VERIFICACIÓN COMPLETADA SATISFACTORIAMENTE")
    print("=" * 70)

if __name__ == '__main__':
    main()
