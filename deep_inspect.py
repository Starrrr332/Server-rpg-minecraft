import sqlite3

def clean_string(s):
    return ''.join(c for c in s if 32 <= ord(c) <= 126)

def analyze_player(name):
    conn = sqlite3.connect('backpack_backup_1790644067.db')
    c = conn.cursor()
    c.execute('SELECT b.itemstacks FROM backpacks b JOIN backpack_players p ON b.owner=p.player_id WHERE p.name=?', (name,))
    row = c.fetchone()
    if not row:
        print(f"No hay datos para {name}")
        return
    
    blob = row[0]
    txt = clean_string(blob.decode('utf-8', errors='ignore'))
    print(f"=== INVENTARIO DE {name} (Tamaño del NBT: {len(blob)} bytes) ===")
    print(txt[:1500])
    print("\n" + "="*50 + "\n")

if __name__ == '__main__':
    for p in ['Stargolden', 'mocosupremo777', '.ElExiliao19', 'Kiruao', 'divk2']:
        analyze_player(p)
