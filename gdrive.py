import json
import streamlit as st
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

# Define Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

# Load credentials from Streamlit secrets
def get_drive_service():
    creds_json = st.secrets["gdrive"]["credentials"]
    creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

# Upload file to Google Drive
def upload_to_drive(file_path, file_name, mime_type='text/csv'):
    service = get_drive_service()
    file_metadata = {'name': file_name, 'parents': ['1EaMX_3vgkdpHRgXvbamDS7UD9D8TMJVX']}  # Replace with your folder ID
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# List files in Google Drive (for debugging)
def list_files():
    service = get_drive_service()
    results = service.files().list().execute()
    return results.get('files', [])
