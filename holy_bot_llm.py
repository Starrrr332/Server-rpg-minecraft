# holy_bot_llm.py
"""Holy Hosting bot with LLM-driven decision making.
The LLM reads a natural-language instruction and decides which action to run:
server status/restart, or file-manager operations (list/read/write/create
folder/delete/rename) via the Pterodactyl API. If the LLM call fails, falls
back to simple keyword detection for status/restart only.
"""
import json
import re
import sys
import requests
import os
from dotenv import load_dotenv

import holy_files

load_dotenv()

CONFIG_PATH = "bot_config.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def api_request(endpoint, method="GET", payload=None):
    cfg = load_config()
    url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}{endpoint}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0",
    }
    response = requests.request(method, url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    if not response.content:
        return {}
    return response.json()


def get_status():
    data = api_request("/resources")
    attrs = data.get("attributes", {})
    res = attrs.get("resources", {})
    uptime_ms = res.get("uptime") or 0
    uptime_s = uptime_ms / 1000
    hours, rem = divmod(int(uptime_s), 3600)
    minutes = rem // 60
    print("=== Server Status ===")
    print(f"State: {attrs.get('current_state')}")
    print(f"Uptime: {hours}h {minutes}m")
    print(f"CPU: {res.get('cpu_absolute', 0):.2f}%")
    print(f"Memory: {res.get('memory_bytes', 0)/1024/1024:.2f} MB")
    print(f"Disk: {res.get('disk_bytes', 0)/1024/1024:.2f} MB")


def restart_server():
    api_request("/power", method="POST", payload={"signal": "restart"})
    print("Restart command sent.")


def send_command(command):
    api_request("/command", method="POST", payload={"command": command})
    print(f"Command sent: {command}")


# -------------------- LLM integration --------------------
SYSTEM_PROMPT = """Eres un asistente que controla un servidor de Minecraft (Pterodactyl) \
y su administrador de archivos. Dada una instruccion en lenguaje natural, responde \
UNICAMENTE con un objeto JSON (sin texto adicional, sin markdown) que describa la accion \
a ejecutar. Las acciones validas son:

{"action": "status"}
{"action": "restart"}
{"action": "list_files", "path": "/ruta"}
{"action": "read_file", "path": "/ruta/archivo.txt"}
{"action": "write_file", "path": "/ruta/archivo.txt", "content": "texto a escribir"}
{"action": "make_folder", "path": "/ruta_base", "name": "nombre_carpeta"}
{"action": "delete_files", "path": "/ruta_base", "files": ["archivo1", "archivo2"]}
{"action": "rename_file", "path": "/ruta_base", "from": "viejo_nombre", "to": "nuevo_nombre"}

Si la ruta no se especifica, usa "/" como raiz. Responde solo con el JSON, nada mas."""


def _extract_json(text):
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise RuntimeError(f"LLM did not return JSON: {text!r}")
    return json.loads(match.group(0))


def decide_action_via_llm(user_prompt):
    cfg = load_config()
    llm_cfg = cfg.get("llm")
    if not llm_cfg:
        raise RuntimeError("LLM configuration not found in bot_config.json")
    provider = llm_cfg.get("provider")
    api_key = llm_cfg.get("api_key")
    model = llm_cfg.get("model")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    if provider == "openai":
        try:
            from openai import OpenAI
        except ImportError:
            raise RuntimeError("openai SDK not installed. Run `pip install openai`.")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(model=model, messages=messages, temperature=0)
        raw = response.choices[0].message.content
    elif provider == "ollama":
        try:
            import ollama
        except ImportError:
            raise RuntimeError("ollama SDK not installed. Run `pip install ollama`.")
        response = ollama.chat(model=model, messages=messages)
        raw = response.get("message", {}).get("content", "")
    elif provider == "huggingface":
        try:
            from huggingface_hub import InferenceClient
        except ImportError:
            raise RuntimeError("huggingface_hub SDK not installed. Run `pip install huggingface_hub`.")
        token = os.getenv("HF_TOKEN")
        model_id = os.getenv("HF_MODEL")
        if not token or not model_id:
            raise RuntimeError("HF_TOKEN or HF_MODEL not set in environment.")
        client = InferenceClient(api_key=token)
        response = client.chat.completions.create(
            model=model_id, messages=messages, max_tokens=300, temperature=0,
        )
        raw = response.choices[0].message.content
    else:
        raise NotImplementedError(f"LLM provider '{provider}' not supported in this demo.")

    return _extract_json(raw)


DESTRUCTIVE_ACTIONS = {
    "restart": "Reiniciar el servidor",
    "write_file": "Escribir/sobrescribir un archivo",
    "make_folder": "Crear una carpeta",
    "delete_files": "ELIMINAR archivo(s)",
    "rename_file": "Renombrar/mover un archivo",
}


def _describe_action(action):
    kind = action.get("action")
    path = action.get("path", "/")
    if kind == "write_file":
        return f"escribir en '{path}' el contenido:\n---\n{action.get('content', '')}\n---"
    if kind == "make_folder":
        return f"crear la carpeta '{action.get('name')}' dentro de '{path}'"
    if kind == "delete_files":
        return f"eliminar {action.get('files', [])} dentro de '{path}'"
    if kind == "rename_file":
        return f"renombrar '{action.get('from')}' a '{action.get('to')}' dentro de '{path}'"
    if kind == "restart":
        return "reiniciar el servidor"
    return str(action)


def confirm_action(action):
    kind = action.get("action")
    label = DESTRUCTIVE_ACTIONS.get(kind)
    if not label:
        return True
    print(f"\n[!] Confirmacion requerida: {label}")
    print(f"   Detalle: {_describe_action(action)}")
    answer = input("Confirmas que quieres ejecutar esta accion? (si/no): ").strip().lower()
    return answer in {"si", "s", "yes", "y"}


def run_action(action):
    kind = action.get("action")
    path = action.get("path", "/")

    if kind in DESTRUCTIVE_ACTIONS and not confirm_action(action):
        print("Accion cancelada por el usuario.")
        return

    if kind == "status":
        get_status()
    elif kind == "restart":
        restart_server()
    elif kind == "list_files":
        holy_files.list_files(path)
    elif kind == "read_file":
        holy_files.read_file(path)
    elif kind == "write_file":
        holy_files.write_file(path, action.get("content", ""))
    elif kind == "make_folder":
        holy_files.make_folder(action.get("name"), root=path)
    elif kind == "delete_files":
        holy_files.delete_files(action.get("files", []), root=path)
    elif kind == "rename_file":
        holy_files.rename_file(action.get("from"), action.get("to"), root=path)
    else:
        raise ValueError(f"Accion desconocida: {kind}")


def main():
    if len(sys.argv) < 2:
        print('Uso: python holy_bot_llm.py "<instruccion>"  # ej. "muestrame los archivos de plugins"')
        sys.exit(1)
    user_instruction = " ".join(sys.argv[1:])

    try:
        action = decide_action_via_llm(user_instruction)
        print(f"LLM decidio ejecutar: {action}")
    except Exception as e:
        print(f"LLM decision failed ({e}); falling back to simple keyword detection.")
        lowered = user_instruction.lower()
        if "status" in lowered or "estado" in lowered:
            action = {"action": "status"}
        elif "restart" in lowered or "reiniciar" in lowered:
            action = {"action": "restart"}
        else:
            print("Unable to infer command. Use 'status' or 'restart'.")
            sys.exit(1)

    try:
        run_action(action)
    except requests.exceptions.HTTPError as e:
        body = e.response.text[:500] if e.response is not None else ""
        print(f"Error HTTP: {e}\n{body}")
        sys.exit(1)


if __name__ == "__main__":
    main()
