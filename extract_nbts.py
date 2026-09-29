import sqlite3

def main():
    conn = sqlite3.connect('backpack_backup_1790644067.db')
    c = conn.cursor()
    c.execute('SELECT p.name, p.uuid, b.itemstacks FROM backpacks b JOIN backpack_players p ON b.owner=p.player_id')
    rows = c.fetchall()
    
    for row in rows:
        name, uuid, blob = row[0], row[1], row[2]
        if len(blob) > 100:
            filename = f"{name}_backpack.dat"
            with open(filename, 'wb') as f:
                f.write(blob)
            print(f"Extraído NBT de {name} ({len(blob)} bytes) -> {filename}")

if __name__ == '__main__':
    main()
