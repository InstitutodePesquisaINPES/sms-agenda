from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configurações
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRET_FILE = 'path/to/your/client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'

# Autorização
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
creds = flow.run_local_server(port=0)

# Construa o serviço do Google Drive
drive_service = build(API_NAME, API_VERSION, credentials=creds)

# Função para enviar um arquivo para o Google Drive
def upload_to_drive(file_path, file_name, folder_id=None):
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = drive_service.files().create(
        body=file_metadata,
        media_body=file_path,
        fields='id'
    ).execute()

    print(f'Arquivo {file_name} enviado para o Google Drive com o ID: {media["id"]}')

