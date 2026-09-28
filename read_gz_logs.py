import os, gzip, glob

log_dir = r"C:\Users\amaro\Downloads\Prism Launcher\instances\Holy RPG 26.2 (Fabric)\minecraft\logs"
gz_files = sorted(glob.glob(os.path.join(log_dir, "*.log.gz")), key=os.path.getmtime, reverse=True)

print(f"Encontrados {len(gz_files)} logs comprimidos.")
for f in gz_files[:3]:
    print(f"\n=== LOG: {os.path.basename(f)} ===")
    try:
        with gzip.open(f, 'rt', encoding='utf-8', errors='ignore') as gz:
            lines = gz.readlines()
            print(f"Total lineas: {len(lines)}")
            for l in lines[-20:]:
                print(" ", l.strip())
    except Exception as e:
        print("Error:", e)
