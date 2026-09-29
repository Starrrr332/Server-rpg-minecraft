# gemini_mc_chat.py
"""
Bot de Minecraft con Gemini AI.
Permite realizar consultas a Google Gemini (gemini-2.5-flash) y transmitir
las respuestas al chat de tu servidor de Minecraft vía la API de Pterodactyl.

Uso:
  1. Configura tu GEMINI_API_KEY en bot_config.json o variable de entorno.
  2. Ejecuta `python gemini_mc_chat.py "Tu pregunta"` para enviar una respuesta de Gemini al chat del servidor.
  3. Ejecuta `python gemini_mc_chat.py listen` para escuchar el chat en tiempo real mediante WebSocket y responder a `!ia` o `!gemini`.
"""

import json
import os
import re
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = "bot_config.json"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"No se encontró {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_gemini_api_key(cfg):
    # Primero busca en bot_config.json under llm.api_key (si provider es gemini) o gemini_api_key o en os.environ
    if cfg.get("llm", {}).get("provider") == "gemini" and cfg.get("llm", {}).get("api_key"):
        return cfg["llm"]["api_key"]
    if cfg.get("gemini_api_key"):
        return cfg["gemini_api_key"]
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return env_key
    raise ValueError(
        "No se encontró la API Key de Gemini. Agrégala en bot_config.json (llm.api_key o gemini_api_key) "
        "o en la variable de entorno GEMINI_API_KEY."
    )


def ask_gemini(prompt: str, system_instruction: str = None) -> str:
    """Consulta la API de Gemini usando el modelo gemini-2.5-flash."""
    cfg = load_config()
    api_key = get_gemini_api_key(cfg)
    model = cfg.get("llm", {}).get("model") or "gemini-2.5-flash"

    if not system_instruction:
        system_instruction = (
            "Eres un asistente amigable y sabio en un servidor de Minecraft RPG. "
            "Responde de manera concisa y clara, apta para leerse en el chat de Minecraft (máximo 2 a 3 frases)."
        )

    # Intento 1: Usar el SDK oficial google-genai
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={"system_instruction": system_instruction}
        )
        if response and response.text:
            return response.text.strip()
    except ImportError:
        pass
    except Exception as e:
        print(f"[SDK Gemini Notice] Usando fallback REST API ({e})")

    # Intento 2: Usar API REST directa (sin librerías adicionales requeridas)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError):
        return "No pude procesar una respuesta de Gemini en este momento."


def send_minecraft_chat(message: str, player_prefix: str = "[Gemini AI]"):
    """Envía un mensaje formateado al chat de Minecraft usando Pterodactyl API."""
    cfg = load_config()
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}/command"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # Limpiar saltos de línea para el comando de minecraft
    clean_msg = message.replace("\n", " ")

    # Construir comando tellraw con formato de colores
    raw_payload = json.dumps([
        {"text": f"{player_prefix} ", "color": "light_purple", "bold": True},
        {"text": clean_msg, "color": "white"}
    ])
    cmd = f"tellraw @a {raw_payload}"

    res = requests.post(base_url, headers=headers, json={"command": cmd}, timeout=10)
    res.raise_for_status()
    print(f"✅ Respuesta enviada a Minecraft: {message[:60]}...")


def listen_pterodactyl_websocket():
    """Escucha la consola de Pterodactyl mediante WebSocket para responder cuando un jugador escribe !ia o !gemini."""
    import websocket
    cfg = load_config()
    base_url = f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Accept": "application/json",
    }

    print("🔌 Solicitando credenciales de WebSocket a Pterodactyl...")
    resp = requests.get(f"{base_url}/ws", headers=headers, timeout=10)
    resp.raise_for_status()
    ws_data = resp.json()["data"]

    token = ws_data["token"]
    socket_url = ws_data["socket"]

    ws = websocket.create_connection(socket_url)
    ws.send(json.dumps({"event": "auth", "args": [token]}))
    print("🤖 Escuchando el chat del servidor de Minecraft... (Usa !ia <pregunta> o !gemini <pregunta>)")

    chat_pattern = re.compile(r"<\s*([^\s>]+)\s*>\s*!(?:ia|gemini)\s+(.+)", re.IGNORECASE)

    try:
        while True:
            msg = ws.recv()
            if not msg:
                continue
            data = json.loads(msg)
            event = data.get("event")
            if event == "console output":
                args = data.get("args", [])
                for line in args:
                    match = chat_pattern.search(line)
                    if match:
                        player = match.group(1)
                        query = match.group(2)
                        print(f"📩 Jugador '{player}' preguntó: {query}")

                        answer = ask_gemini(
                            prompt=f"El jugador '{player}' en el servidor de Minecraft te pregunta: {query}",
                            system_instruction="Eres el bot asistente de IA del servidor de Minecraft. Responde en 1-2 frases para el chat."
                        )
                        send_minecraft_chat(answer, player_prefix=f"[Gemini ➔ {player}]")
    except KeyboardInterrupt:
        print("\nDesconectando listener...")
    finally:
        ws.close()


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python gemini_mc_chat.py \"<tu pregunta>\"   - Preguntar a Gemini y enviar al chat")
        print("  python gemini_mc_chat.py listen          - Escuchar en vivo !ia en el chat del servidor")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd.lower() == "listen":
        listen_pterodactyl_websocket()
    else:
        prompt = " ".join(sys.argv[1:])
        print(f"Consultando a Gemini: '{prompt}'...")
        res = ask_gemini(prompt)
        print(f"\nRespuesta de Gemini:\n{res}\n")
        send_minecraft_chat(res)


if __name__ == "__main__":
    main()
