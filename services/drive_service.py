import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseUpload
import io
import mimetypes


# Initialize Google Drive API client
def get_drive_service():
    try:
        # Get credentials from Streamlit secrets
        creds_dict = st.secrets["google"]
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        st.error(f"Error initializing Drive service: {str(e)}")
        raise


# Create or get folder ID
def get_or_create_folder(drive_service, folder_name, parent_folder_id = st.secrets["drive"]["parent_folder_id"]):
    try:
        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"
        
        response = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        folders = response.get('files', [])
        
        if folders:
            return folders[0]['id']
        
        # Create new folder if it doesn't exist
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_folder_id:
            folder_metadata['parents'] = [parent_folder_id]
            
        folder = drive_service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        return folder.get('id')
    except Exception as e:
        st.error(f"Error managing folder: {str(e)}")
        raise


def upload_file(file_uploaded, folder_name, student_number, parent_folder_id = st.secrets["drive"]["parent_folder_id"]):
    try:
        drive_service = get_drive_service()
        
        # Create/get the specified   folder in Google Drive
        uploads_folder_id = get_or_create_folder(drive_service, folder_name, parent_folder_id)

        # Get file extension from the uploaded file
        file_extension = file_uploaded.name.split('.')[-1]
        full_file_name = f"{student_number}.{file_extension}"
        
        # Read file content
        file_content = file_uploaded.getvalue()
        
        # Detect MIME type dynamically
        mime_type, _ = mimetypes.guess_type(file_uploaded.name)
        if not mime_type:
            mime_type = "application/octet-stream"  # Default for unknown file types
        
        # Prepare file metadata
        file_metadata = {
            'name': full_file_name,
            'parents': [uploads_folder_id],
        }
        
        # Upload file using MediaIoBaseUpload
        media = MediaIoBaseUpload(
            io.BytesIO(file_content),
            mimetype=mime_type,
            resumable=True
        )
        
        # Create file in Drive
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()
        
        # Make file publicly accessible
        drive_service.permissions().create(
            fileId=file.get('id'),
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        
        return file.get('webViewLink')
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        raise



def search_file(folder_name, student_number, parent_folder_id = st.secrets["drive"]["parent_folder_id"]):
    try:
        drive_service = get_drive_service()

        # Create/get the specified  folder in Google Drive
        uploads_folder_id = get_or_create_folder(drive_service, folder_name, parent_folder_id)

        query = f"name contains '{student_number}' and '{uploads_folder_id}' in parents"

        response = drive_service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, webViewLink)'
        ).execute()

        files = response.get('files', [])
        
        if files:
            return files[0]['webViewLink']
        else:
            return None
        
    except Exception as e:
            st.error(f"Error searching file: {str(e)}")
            raise