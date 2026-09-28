import os
import json
import time
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'service_account.json')
TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'token.json')
DRIVE_FOLDER_NAME = "HolyServer_Backups"

class GoogleDriveManager:
    def __init__(self):
        self.service = None
        self.folder_id = None

    def authenticate(self):
        """Autentica con Google Drive mediante Service Account o OAuth2 Credentials."""
        creds = None
        
        # 1. Probar Service Account
        if os.path.exists(SERVICE_ACCOUNT_FILE):
            try:
                creds = service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive']
                )
                self.service = build('drive', 'v3', credentials=creds)
                print("[Google Drive] Autenticado mediante Cuenta de Servicio (service_account.json).")
                return True
            except Exception as e:
                print(f"[Google Drive] Error cargando service_account.json: {e}")

        # 2. Probar Token OAuth2 existente
        if os.path.exists(TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            except Exception as e:
                print(f"[Google Drive] Error leyendo token.json: {e}")

        # 3. Refrescar o solicitar nuevo Token OAuth2
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(TOKEN_FILE, 'w') as token:
                        token.write(creds.to_json())
                    print("[Google Drive] Token de acceso actualizado exitosamente.")
                except Exception as e:
                    print(f"[Google Drive] Error al refrescar token: {e}")
                    creds = None

            if not creds:
                if not os.path.exists(CREDENTIALS_FILE):
                    print("[Google Drive] AVISO: No se encontro 'credentials.json' ni 'service_account.json'.")
                    print("Por favor coloca el archivo credentials.json de tu consola Google Cloud para activar la subida directa.")
                    return False
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                    creds = flow.run_local_server(port=0)
                    with open(TOKEN_FILE, 'w') as token:
                        token.write(creds.to_json())
                    print("[Google Drive] Nueva sesion OAuth2 iniciada y guardada en token.json.")
                except Exception as e:
                    print(f"[Google Drive] Error al iniciar flujo OAuth2: {e}")
                    return False

        try:
            self.service = build('drive', 'v3', credentials=creds)
            return True
        except Exception as e:
            print(f"[Google Drive] Error al inicializar cliente Drive API: {e}")
            return False

    def get_or_create_folder(self):
        """Busca o crea la carpeta de backups en Google Drive."""
        if not self.service:
            if not self.authenticate():
                return None

        try:
            query = f"name = '{DRIVE_FOLDER_NAME}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])

            if files:
                self.folder_id = files[0]['id']
                return self.folder_id
            else:
                folder_metadata = {
                    'name': DRIVE_FOLDER_NAME,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(body=folder_metadata, fields='id').execute()
                self.folder_id = folder.get('id')
                print(f"[Google Drive] Carpeta creada: '{DRIVE_FOLDER_NAME}' (ID: {self.folder_id})")
                return self.folder_id
        except Exception as e:
            print(f"[Google Drive] Error buscando/creando carpeta: {e}")
            return None

    def upload_file(self, local_filepath, max_retention=5):
        """Sube un archivo a Google Drive y rota copias antiguas."""
        folder_id = self.get_or_create_folder()
        if not folder_id:
            print("[Google Drive] No se pudo obtener la carpeta destino en Drive.")
            return False

        filename = os.path.basename(local_filepath)
        file_size_mb = os.path.getsize(local_filepath) / (1024 * 1024)
        print(f"[Google Drive] Subiendo '{filename}' ({file_size_mb:.2f} MB) a la carpeta '{DRIVE_FOLDER_NAME}'...")

        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(local_filepath, resumable=True)

        try:
            uploaded_file = self.service.files().create(
                body=file_metadata, media_body=media, fields='id, name, webViewLink'
            ).execute()
            print(f"[Google Drive] Subida exitosa! ID: {uploaded_file.get('id')}")
            print(f"[Google Drive] Enlace: {uploaded_file.get('webViewLink')}")

            # Rotar copias antiguas
            self.enforce_retention(max_retention)
            return uploaded_file
        except Exception as e:
            print(f"[Google Drive] Error al subir archivo: {e}")
            return False

    def enforce_retention(self, max_retention=5):
        """Mantiene solo las ultimas N copias de seguridad en Google Drive."""
        if not self.folder_id or not self.service:
            return

        try:
            query = f"'{self.folder_id}' in parents and trashed = false"
            results = self.service.files().list(
                q=query, spaces='drive', fields='files(id, name, createdTime)', orderBy='createdTime desc'
            ).execute()
            files = results.get('files', [])

            if len(files) > max_retention:
                to_delete = files[max_retention:]
                print(f"[Google Drive] Rotando backups ({len(to_delete)} copias antiguas seran eliminadas)...")
                for f in to_delete:
                    self.service.files().delete(fileId=f['id']).execute()
                    print(f"  - Eliminado de Drive: {f['name']} ({f['createdTime']})")
        except Exception as e:
            print(f"[Google Drive] Error en la rotacion de backups: {e}")

if __name__ == '__main__':
    mgr = GoogleDriveManager()
    if mgr.authenticate():
        fid = mgr.get_or_create_folder()
        print(f"Prueba de conexion exitosa. ID de Carpeta: {fid}")
    else:
        print("Autenticacion pendiente. Sigue la guia en INSTRUCCIONES_GOOGLE_DRIVE.md")
