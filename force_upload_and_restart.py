import holy_files
import holy_bot_llm
import os
import requests
import time

cfg = holy_files.load_config()
base_url = holy_files._base_url(cfg)
headers = holy_files._headers(cfg)

local_jar = "GuildAIEconomy-1.0.0.jar"
jar_size = os.path.getsize(local_jar)
print(f"[1/5] Tamaño del JAR local a subir: {jar_size} bytes")

# Paso 1: Eliminar archivos antiguos del servidor
print("[2/5] Eliminando versión antigua en /plugins/ y raíz...")
try:
    holy_files.delete_files(["GuildAIEconomy-1.0.0.jar"], root="/plugins")
except Exception as e:
    print("  Info:", e)

try:
    holy_files.delete_files(["GuildAIEconomy-1.0.0.jar"], root="/")
except Exception as e:
    print("  Info:", e)

# Paso 2: Obtener URL firmada de subida para /plugins
print("[3/5] Obteniendo URL de subida para /plugins...")
resp = requests.get(f"{base_url}/files/upload", headers=headers, params={"directory": "/plugins"}, timeout=30)
resp.raise_for_status()
data = resp.json()
signed_url = data.get('attributes', {}).get('url') or data.get('data', {}).get('attributes', {}).get('url')

# Paso 3: Subir nuevo JAR
print(f"[4/5] Subiendo {local_jar} ({jar_size} bytes) a /plugins...")
with open(local_jar, 'rb') as f:
    files = {'files': (local_jar, f, 'application/java-archive')}
    upload_resp = requests.post(signed_url, files=files, timeout=120)
    upload_resp.raise_for_status()

print("[5/5] Verificando archivo subido en /plugins...")
plugins_files = holy_files.list_files('/plugins')
uploaded = [f for f in plugins_files if f['attributes']['name'] == local_jar]
if uploaded:
    print(f"  [EXITO] Archivo subido correctamente: {uploaded[0]['attributes']['name']} ({uploaded[0]['attributes']['size']} bytes)")
else:
    print("  [ERROR] No se encontró el archivo en /plugins tras la subida.")

# Reinicio del servidor
print("\n🔄 Reiniciando servidor para aplicar actualización...")
holy_bot_llm.restart_server()
