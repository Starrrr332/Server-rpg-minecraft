import requests
import json

def setup_panel_schedule():
    with open('bot_config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    headers = {
        'Authorization': f"Bearer {cfg['api_key']}",
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 HolyBot/1.0'
    }

    # Create schedule
    payload = {
        "name": "Auto Save & Sync Stats",
        "is_active": True,
        "minute": "*/30",
        "hour": "*",
        "day_of_month": "*",
        "month": "*",
        "day_of_week": "*",
        "only_when_online": True
    }

    r = requests.post(
        f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/schedules",
        headers=headers,
        json=payload,
        timeout=15
    )
    print("Create Schedule status:", r.status_code)
    if r.status_code in [200, 201]:
        schedule_id = r.json()['attributes']['id']
        print(f"Schedule creado con ID {schedule_id}. Anadiendo tarea 'save-all'...")
        
        # Add task to execute console command 'save-all'
        task_payload = {
            "action": "command",
            "payload": "save-all",
            "time_offset": 0,
            "continue_on_failure": False
        }
        r_task = requests.post(
            f"{cfg['panel_url']}/api/client/servers/{cfg['server_id']}/schedules/{schedule_id}/tasks",
            headers=headers,
            json=task_payload,
            timeout=15
        )
        print("Task status:", r_task.status_code)
        if r_task.status_code in [200, 201]:
            print("[OK] Cronjob en el panel de Holy Hosting configurado con exito cada 30 minutos.")
    else:
        print("Response:", r.text[:300])

if __name__ == '__main__':
    setup_panel_schedule()
