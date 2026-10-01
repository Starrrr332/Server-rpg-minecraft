# -*- coding: utf-8 -*-
import glob
import re
import json

def parse_minecraft_colors(text):
    if not text:
        return ""
    # Map Minecraft color codes &0-9, &a-f, &k-r to HTML style spans
    color_map = {
        '0': '#000000', '1': '#0000aa', '2': '#00aa00', '3': '#00aaaa',
        '4': '#aa0000', '5': '#aa00aa', '6': '#ffaa00', '7': '#aaaaaa',
        '8': '#555555', '9': '#5555ff', 'a': '#55ff55', 'b': '#55ffff',
        'c': '#ff5555', 'd': '#ff55ff', 'e': '#ffff55', 'f': '#ffffff',
        'r': '#ffffff'
    }
    
    # Replace &x codes
    result = []
    parts = re.split(r'&([0-9a-frk-o])', text)
    current_color = '#ffffff'
    is_bold = False
    
    i = 0
    while i < len(parts):
        if i == 0:
            if parts[i]:
                result.append(f'<span style="color:{current_color}">{parts[i]}</span>')
            i += 1
            continue
        
        code = parts[i]
        val = parts[i+1] if i+1 < len(parts) else ""
        if code in color_map:
            current_color = color_map[code]
        elif code == 'l':
            is_bold = True
        
        bold_style = 'font-weight:bold;' if is_bold else ''
        if val:
            result.append(f'<span style="color:{current_color};{bold_style}">{val}</span>')
        i += 2
        
    return "".join(result)

def parse_item_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    mat_match = re.search(r'material:\s*([A-Z0-9_]+)', content)
    name_match = re.search(r'name:\s*[\'\"]?(.*?)[\'\"]?\n', content)
    
    material = mat_match.group(1) if mat_match else 'STONE'
    raw_name = name_match.group(1).strip() if name_match else filepath.split('/')[-1]
    
    # Extract lore lines
    lore_lines = []
    in_lore = False
    for line in content.splitlines():
        if line.strip().startswith('lore:'):
            in_lore = True
            continue
        if in_lore:
            if line.strip().startswith('-'):
                clean_line = line.strip()[1:].strip().strip("'\"")
                lore_lines.append(clean_line)
            elif line.strip() and not line.startswith(' '):
                in_lore = False
                
    # Extract enchantments
    enchants = []
    in_ench = False
    for line in content.splitlines():
        if line.strip().startswith('enchantments:'):
            in_ench = True
            continue
        if in_ench:
            if line.strip().startswith('-'):
                clean_e = line.strip()[1:].strip().strip("'\"")
                enchants.append(clean_e)
            elif line.strip() and not line.startswith(' '):
                in_ench = False

    return {
        'id': filepath.split('/')[-1].replace('.yml', ''),
        'material': material,
        'raw_name': raw_name,
        'html_name': parse_minecraft_colors(raw_name),
        'lore_raw': lore_lines,
        'html_lore': [parse_minecraft_colors(l) for l in lore_lines],
        'enchantments': enchants
    }

def main():
    items = []
    for f in glob.glob('customitems/*.yml'):
        items.append(parse_item_file(f.replace('\\', '/')))
    print(f"Total Custom Items parsed: {len(items)}")
    print(json.dumps(items[:2], indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
