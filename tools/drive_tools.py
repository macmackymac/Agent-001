"""
Google Drive tool functions for APPA.
"""

from services.drive_service import DriveService

TOOL_ERROR = "TOOL_ERROR:"


def save_to_google_drive(
    google_authenticated,
    google_credentials,
    filename: str,
    content: str,
) -> str:
    """
    Save a text file to Google Drive.
    """

    if not google_authenticated or not google_credentials:
        return (
            f"{TOOL_ERROR} Google Drive not authenticated. "
            "Connect in the sidebar first."
        )

    try:
        drive = DriveService(
            google_credentials
        )

        file = drive.upload_text_file(
            filename,
            content,
        )

        return (
            f"✅ File '{file['name']}' uploaded successfully.\n\n"
            f"Drive File ID: {file['id']}\n"
            f"Link: {file['webViewLink']}"
        )

    except Exception as exc:
        return f"{TOOL_ERROR} could not save to Drive: {exc}"
