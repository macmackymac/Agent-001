"""
Gmail tool functions for APPA.
"""

from services.gmail_service import GmailService

TOOL_ERROR = "TOOL_ERROR:"


def read_recent_emails(google_authenticated, google_credentials, max_results=5):
    """
    Read recent unread emails from Gmail.
    """

    if not google_authenticated or not google_credentials:
        return (
            f"{TOOL_ERROR} Gmail not authenticated. "
            "Connect in the sidebar first."
        )

    try:
        gmail = GmailService(
            google_credentials
        )

        emails = gmail.get_unread_messages(max_results)

        if not emails:
            return "No unread emails found."

        output = []

        for email in emails:
            output.append(
                f"From: {email['sender']}\n"
                f"Subject: {email['subject']}"
            )

        return "\n\n".join(output)

    except Exception as exc:
        return f"{TOOL_ERROR} could not read emails: {exc}"
