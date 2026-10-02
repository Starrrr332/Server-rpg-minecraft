import json
import requests

def update_chunky_config():
    with open("bot_config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}

    # Fetch Chunky config.yml
    r = requests.get(f"{base_url}/files/contents", headers=headers, params={'file': 'plugins/Chunky/config.yml'}, timeout=10)
    if r.status_code == 200:
        content = r.text
        print("--- CURRENT CHUNKY CONFIG ---")
        print(content)

        # Ensure continue-on-restart: true
        new_content = content.replace("continue-on-restart: false", "continue-on-restart: true")
        if "continue-on-restart:" not in new_content:
            new_content += "\ncontinue-on-restart: true\n"

        if new_content != content:
            print("\nUpdating Chunky config.yml to set continue-on-restart: true...")
            # Save file
            save_resp = requests.post(f"{base_url}/files/write", headers={**headers, "Content-Type": "text/plain"}, params={'file': 'plugins/Chunky/config.yml'}, data=new_content, timeout=10)
            print("Save response status:", save_resp.status_code)
        else:
            print("\ncontinue-on-restart is already true.")

        # Also send chunky reload to console
        requests.post(f"{base_url}/command", headers={**headers, "Content-Type": "application/json"}, json={'command': 'chunky reload'}, timeout=10)
        print("Sent 'chunky reload' command.")
    else:
        print("Failed to read plugins/Chunky/config.yml:", r.status_code, r.text)

if __name__ == '__main__':
    update_chunky_config()
