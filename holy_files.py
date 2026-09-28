# holy_files.py
"""File manager for the Pterodactyl server, using the same bot_config.json
credentials as holy_bot_llm.py.

Usage:
    python holy_files.py ls [directory]
    python holy_files.py cat <file>
    python holy_files.py write <file> <local_source_or_->
    python holy_files.py mkdir <directory>
    python holy_files.py rm <file1> [file2 ...]
    python holy_files.py mv <from> <to>
"""
import json
import sys
import requests

CONFIG_PATH = "bot_config.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _base_url(cfg):
    return f"{cfg['panel_url'].rstrip('/')}/api/client/servers/{cfg['server_id']}"


def _headers(cfg, content_type=None):
    headers = {
        "Authorization": f"Bearer {cfg['api_key']}",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HolyBot/1.0",
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def list_files(directory="/"):
    cfg = load_config()
    url = f"{_base_url(cfg)}/files/list"
    resp = requests.get(url, headers=_headers(cfg), params={"directory": directory}, timeout=15)
    resp.raise_for_status()
    data = resp.json().get("data", [])
    print(f"=== Contenido de {directory} ===")
    for item in data:
        attrs = item.get("attributes", {})
        kind = "DIR " if attrs.get("is_file") is False else "FILE"
        size = attrs.get("size", 0)
        print(f"[{kind}] {attrs.get('name'):<40} {size} bytes")
    return data


def read_file(path):
    cfg = load_config()
    url = f"{_base_url(cfg)}/files/contents"
    resp = requests.get(url, headers=_headers(cfg), params={"file": path}, timeout=15)
    resp.raise_for_status()
    print(resp.text)
    return resp.text


def write_file(path, content):
    cfg = load_config()
    url = f"{_base_url(cfg)}/files/write"
    resp = requests.post(
        url,
        headers=_headers(cfg, content_type="text/plain"),
        params={"file": path},
        data=content.encode("utf-8"),
        timeout=15,
    )
    resp.raise_for_status()
    print(f"Archivo '{path}' escrito correctamente.")


def make_folder(name, root="/"):
    cfg = load_config()
    url = f"{_base_url(cfg)}/files/create-folder"
    resp = requests.post(
        url,
        headers=_headers(cfg, content_type="application/json"),
        json={"root": root, "name": name},
        timeout=15,
    )
    resp.raise_for_status()
    print(f"Carpeta '{name}' creada en '{root}'.")


def delete_files(paths, root="/"):
    cfg = load_config()
    url = f"{_base_url(cfg)}/files/delete"
    resp = requests.post(
        url,
        headers=_headers(cfg, content_type="application/json"),
        json={"root": root, "files": paths},
        timeout=15,
    )
    resp.raise_for_status()
    print(f"Eliminado(s): {', '.join(paths)}")


def rename_file(from_path, to_path, root="/"):
    cfg = load_config()
    url = f"{_base_url(cfg)}/files/rename"
    resp = requests.put(
        url,
        headers=_headers(cfg, content_type="application/json"),
        json={"root": root, "files": [{"from": from_path, "to": to_path}]},
        timeout=15,
    )
    resp.raise_for_status()
    print(f"Renombrado '{from_path}' -> '{to_path}'.")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    action = sys.argv[1]
    args = sys.argv[2:]

    try:
        if action == "ls":
            list_files(args[0] if args else "/")
        elif action == "cat":
            if not args:
                print("Uso: python holy_files.py cat <archivo>")
                sys.exit(1)
            read_file(args[0])
        elif action == "write":
            if len(args) < 2:
                print("Uso: python holy_files.py write <archivo_remoto> <archivo_local_o_->")
                sys.exit(1)
            remote_path, source = args[0], args[1]
            if source == "-":
                content = sys.stdin.read()
            else:
                with open(source, "r", encoding="utf-8") as f:
                    content = f.read()
            write_file(remote_path, content)
        elif action == "mkdir":
            if not args:
                print("Uso: python holy_files.py mkdir <carpeta>")
                sys.exit(1)
            make_folder(args[0])
        elif action == "rm":
            if not args:
                print("Uso: python holy_files.py rm <archivo1> [archivo2 ...]")
                sys.exit(1)
            delete_files(args)
        elif action == "mv":
            if len(args) < 2:
                print("Uso: python holy_files.py mv <origen> <destino>")
                sys.exit(1)
            rename_file(args[0], args[1])
        else:
            print(__doc__)
            sys.exit(1)
    except requests.exceptions.HTTPError as e:
        body = e.response.text[:500] if e.response is not None else ""
        print(f"Error HTTP: {e}\n{body}")
        sys.exit(1)


if __name__ == "__main__":
    main()
