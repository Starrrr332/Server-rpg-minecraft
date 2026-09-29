import sqlite3
import re
import json

def parse_nbt_items(blob):
    text = blob.decode('utf-8', errors='ignore')
    # Find all occurrences of minecraft:id followed by counts/components
    matches = re.findall(r'id\x00\x10minecraft:([a-z0-9_]+)', text)
    if not matches:
        matches = re.findall(r'minecraft:([a-z0-9_]+)', text)
    
    # Filter out component keywords
    ignored = {'custom_data', 'custom_name', 'lore', 'attribute_modifiers', 'enchantments', 
               'tooltip_display', 'attack_damage', 'attack_speed', 'enchantment_glint_override',
               'potion_contents', 'stored_enchantments', 'container', 'damage', 'ominous_bottle_amplifier'}
    
    clean_items = [m for m in matches if m not in ignored]
    return clean_items

def main():
    conn = sqlite3.connect('backpack_backup_1790644067.db')
    c = conn.cursor()
    c.execute('SELECT p.name, p.uuid, b.itemstacks FROM backpacks b JOIN backpack_players p ON b.owner=p.player_id')
    rows = c.fetchall()
    
    player_inventories = {}
    for row in rows:
        name, uuid, blob = row[0], row[1], row[2]
        items = parse_nbt_items(blob)
        if items:
            player_inventories[name] = items

    print(json.dumps(player_inventories, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
