# -*- coding: utf-8 -*-
"""
Script de sincronización de Cuentas de Jugadores en MySQL de Holy Hosting.
Vincula cada jugador de Minecraft con una cuenta en la base de datos SQL del servidor.
"""
import json
import os
import hashlib
import pymysql

def get_connection(cfg):
    db_cfg = cfg['database']
    return pymysql.connect(
        host=db_cfg['host'],
        port=db_cfg['port'],
        user=db_cfg['user'],
        password=db_cfg['password'],
        database=db_cfg['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10
    )

def setup_table(conn):
    schema_sql = """
    CREATE TABLE IF NOT EXISTS player_accounts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        uuid VARCHAR(36) NOT NULL UNIQUE,
        username VARCHAR(64) NOT NULL UNIQUE,
        is_bedrock BOOLEAN DEFAULT FALSE,
        avatar_url VARCHAR(255),
        play_time_seconds INT DEFAULT 0,
        play_time_formatted VARCHAR(32) DEFAULT '0m',
        auraskills_level INT DEFAULT 0,
        auraskills_avg FLOAT DEFAULT 0.0,
        mob_kills INT DEFAULT 0,
        player_kills INT DEFAULT 0,
        deaths INT DEFAULT 0,
        kdr FLOAT DEFAULT 0.0,
        blocks_mined INT DEFAULT 0,
        items_crafted INT DEFAULT 0,
        distance_km FLOAT DEFAULT 0.0,
        mana FLOAT DEFAULT 0.0,
        auth_token VARCHAR(64) NOT NULL UNIQUE,
        role VARCHAR(32) DEFAULT 'player',
        status VARCHAR(32) DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        INDEX idx_username (username),
        INDEX idx_auraskills (auraskills_level),
        INDEX idx_playtime (play_time_seconds)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    with conn.cursor() as cur:
        cur.execute(schema_sql)
    conn.commit()
    print("[OK] Tabla 'player_accounts' verificada/creada exitosamente en MySQL.")

def generate_auth_token(uuid, username):
    salt = "holy_server_rpg_salt_2026"
    return hashlib.sha256(f"{uuid}:{username}:{salt}".encode('utf-8')).hexdigest()[:24]

def sync_accounts():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    stats_path = 'dist/stats_data.json'
    if not os.path.exists(stats_path):
        print("[!] No se encontro dist/stats_data.json. Ejecuta primero build_database.py.")
        return

    with open(stats_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    players = data.get('players', [])
    print(f"Sincronizando {len(players)} jugadores con la base de datos SQL de Holy Hosting...")

    conn = get_connection(cfg)
    try:
        setup_table(conn)

        upsert_sql = """
        INSERT INTO player_accounts (
            uuid, username, is_bedrock, avatar_url, play_time_seconds,
            play_time_formatted, auraskills_level, auraskills_avg,
            mob_kills, player_kills, deaths, kdr, blocks_mined,
            items_crafted, distance_km, mana, auth_token, role
        ) VALUES (
            %(uuid)s, %(username)s, %(is_bedrock)s, %(avatar_url)s, %(play_time_seconds)s,
            %(play_time_formatted)s, %(auraskills_level)s, %(auraskills_avg)s,
            %(mob_kills)s, %(player_kills)s, %(deaths)s, %(kdr)s, %(blocks_mined)s,
            %(items_crafted)s, %(distance_km)s, %(mana)s, %(auth_token)s, %(role)s
        )
        ON DUPLICATE KEY UPDATE
            username = VALUES(username),
            is_bedrock = VALUES(is_bedrock),
            avatar_url = VALUES(avatar_url),
            play_time_seconds = VALUES(play_time_seconds),
            play_time_formatted = VALUES(play_time_formatted),
            auraskills_level = VALUES(auraskills_level),
            auraskills_avg = VALUES(auraskills_avg),
            mob_kills = VALUES(mob_kills),
            player_kills = VALUES(player_kills),
            deaths = VALUES(deaths),
            kdr = VALUES(kdr),
            blocks_mined = VALUES(blocks_mined),
            items_crafted = VALUES(items_crafted),
            distance_km = VALUES(distance_km),
            mana = VALUES(mana),
            updated_at = CURRENT_TIMESTAMP;
        """

        synced_count = 0
        with conn.cursor() as cur:
            for p in players:
                token = generate_auth_token(p['uuid'], p['name'])
                # Owner role for Stargolden
                role = 'admin' if p['name'].lower() == 'stargolden' else 'player'

                params = {
                    'uuid': p['uuid'],
                    'username': p['name'],
                    'is_bedrock': 1 if p.get('is_bedrock') else 0,
                    'avatar_url': p.get('avatar', ''),
                    'play_time_seconds': p.get('play_time_seconds', 0),
                    'play_time_formatted': p.get('play_time_str', '0m'),
                    'auraskills_level': p.get('total_skill_level', 0),
                    'auraskills_avg': p.get('skill_average', 0.0),
                    'mob_kills': p.get('mob_kills', 0),
                    'player_kills': p.get('player_kills', 0),
                    'deaths': p.get('deaths', 0),
                    'kdr': p.get('kdr', 0.0),
                    'blocks_mined': p.get('total_mined', 0),
                    'items_crafted': p.get('total_crafted', 0),
                    'distance_km': p.get('distances', {}).get('total_km', 0.0),
                    'mana': p.get('mana', 0.0),
                    'auth_token': token,
                    'role': role
                }
                cur.execute(upsert_sql, params)
                synced_count += 1

        conn.commit()
        print(f"[EXITO] {synced_count} cuentas vinculadas y actualizadas en MySQL.")

        # Show preview
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, auraskills_level, play_time_formatted, auth_token, role FROM player_accounts ORDER BY play_time_seconds DESC LIMIT 5;")
            rows = cur.fetchall()
            print("\n--- Vista previa de cuentas en MySQL ---")
            for r in rows:
                print(f"ID #{r['id']} | {r['username']} (Rol: {r['role']}) | AuraSkills: Lvl {r['auraskills_level']} | Tiempo: {r['play_time_formatted']} | Token: {r['auth_token']}")

    finally:
        conn.close()

if __name__ == '__main__':
    sync_accounts()
