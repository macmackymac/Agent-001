from io import BytesIO

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


class DriveService:
    def __init__(self, credentials):
        self.service = build("drive", "v3", credentials=credentials)

    def upload_text_file(self, filename: str, content: str):

        file_metadata = {
            "name": filename
        }

        media = MediaIoBaseUpload(
            BytesIO(content.encode("utf-8")),
            mimetype="text/plain",
            resumable=False,
        )

        file = (
            self.service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id,name,webViewLink",
            )
            .execute()
        )

        return file
