import json
import os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

# Load Google Drive credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path, file_name, mime_type='text/csv'):
    file_metadata = {'name': file_name, 'parents': ['1EaMX_3vgkdpHRgXvbamDS7UD9D8TMJVX']}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded File ID: {file.get('id')}")
    return file.get('id')

def list_files():
    results = service.files().list().execute()
    for file in results.get('files', []):
        print(f"{file['name']} ({file['id']})")