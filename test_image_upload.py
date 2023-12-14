import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# Set your credentials JSON file path
creds_path = 'client_secret.json'

# Set your Google Drive folder ID
folder_id = '1CoS2eDqIhlwHVWAJ0BOH_BSMOJKN6YRL'

# If modifying these, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def upload_image(service, image_path, folder_id):
    media = MediaFileUpload(image_path, mimetype='image/jpg')
    file_metadata = {'name': os.path.basename(image_path), 'parents': [folder_id]}
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')

def download_image(service, file_id, destination_path):
    request = service.files().get_media(fileId=file_id)
    with open(destination_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%")

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        creds = get_credentials()
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Example: Upload an image
    upload_image(service, 'google_logo.jpg', folder_id)

    # Example: Download an image
    # download_image(service, 'your_file_id', 'path/to/your/destination/image.jpg')

if __name__ == '__main__':
    main()
