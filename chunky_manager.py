"""
Chunky Auto-Manager Daemon para HolyServer.
Monitorea continuamente la cantidad de jugadores conectados.
- Si hay 0 jugadores: Activa/Reanuda el pre-generado de mapa con Chunky ('chunky start').
- Si hay 1 o más jugadores: Pausa inmediatamente Chunky ('chunky pause') para evitar lag.
"""
import time
import json
import logging
import requests

CONFIG_PATH = "bot_config.json"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chunky_manager.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def send_command(cfg, command):
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        resp = requests.post(f"{base_url}/command", headers=headers, json={"command": command}, timeout=10)
        return resp.status_code == 204
    except Exception as e:
        logging.error(f"Error enviando comando '{command}': {e}")
        return False

def get_server_stats(cfg):
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Accept": "application/json"
    }
    try:
        resp = requests.get(f"{base_url}/resources", headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json().get('attributes', {})
    except Exception as e:
        logging.error(f"Error consultando servidor: {e}")
    return None

def check_online_players_mcstatus():
    """Query public server IP for real-time online player count."""
    try:
        r = requests.get("https://api.mcstatus.io/v2/status/java/38.97.61.71:19618", timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get('online'):
                return data.get('players', {}).get('online', 0)
    except Exception:
        pass
    return 0

def main():
    cfg = load_config()
    logging.info("=== Chunky Auto-Manager Iniciado ===")
    
    # Pre-configuración de Chunky
    send_command(cfg, "chunky world world")
    send_command(cfg, "chunky shape circle")
    send_command(cfg, "chunky radius 5000")
    send_command(cfg, "chunky quiet 30")
    logging.info("Chunky configurado: Mundo 'world', Círculo, Radio 5000 bloques.")

    chunky_running = False

    while True:
        try:
            stats = get_server_stats(cfg)
            if stats and stats.get('current_state') == 'running':
                players = check_online_players_mcstatus()
                
                if players > 0:
                    if chunky_running:
                        logging.info(f"Jugador(es) detectado(s) ({players} online). Pausando Chunky...")
                        send_command(cfg, "chunky pause")
                        chunky_running = False
                    else:
                        logging.info(f"Servidor ocupado ({players} jugadores online). Chunky permanece pausado.")
                else:
                    if not chunky_running:
                        logging.info("0 jugadores conectados. Activando pre-carga de mapa con Chunky...")
                        send_command(cfg, "chunky start")
                        chunky_running = True
                    else:
                        logging.info("0 jugadores conectados. Chunky pre-generando mapa en segundo plano...")
            else:
                chunky_running = False

            time.sleep(20)
        except KeyboardInterrupt:
            logging.info("Chunky Auto-Manager detenido.")
            break
        except Exception as e:
            logging.error(f"Error en ciclo: {e}")
            time.sleep(20)

if __name__ == "__main__":
    main()
