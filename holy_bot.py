# holy_bot.py
"""Simple Holy Hosting bot.
Provides two commands via the command line:
  python holy_bot.py status   – get server status
  python holy_bot.py restart  – send a restart command

Configuration is read from `bot_config.json` in the same directory.
"""
import json
import sys
import requests

CONFIG_PATH = "bot_config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def api_request(endpoint, method="GET", payload=None):
    cfg = load_config()
    url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}{endpoint}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    response = requests.request(method, url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

def get_status():
    data = api_request("/resources")
    attributes = data.get("attributes", {})
    print("=== Server Status ===")
    print(f"Name: {attributes.get('name')}")
    print(f"State: {attributes.get('current_state')}")
    print(f"Uptime: {attributes.get('uptime')}")
    print(f"CPU: {attributes.get('cpu_absolute'):.2f}%")
    print(f"Memory: {attributes.get('memory_bytes')/1024/1024:.2f} MB")
    print(f"Disk: {attributes.get('disk_bytes')/1024/1024:.2f} MB")

def restart_server():
    api_request("/power", method="POST", payload={"signal": "restart"})
    print("Restart command sent.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python holy_bot.py [status|restart]")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "status":
        get_status()
    elif cmd == "restart":
        restart_server()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
