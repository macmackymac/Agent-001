from googleapiclient.discovery import build


class GmailService:
    def __init__(self, credentials):
        self.service = build("gmail", "v1", credentials=credentials)

    def get_unread_messages(self, max_results=5):
        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                maxResults=max_results,
                q="is:unread"
            )
            .execute()
        )

        messages = results.get("messages", [])

        if not messages:
            return []

        emails = []

        for msg in messages:
            message = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"]
                )
                .execute()
            )

            headers = message["payload"].get("headers", [])

            subject = next(
                (
                    h["value"]
                    for h in headers
                    if h["name"] == "Subject"
                ),
                "No subject",
            )

            sender = next(
                (
                    h["value"]
                    for h in headers
                    if h["name"] == "From"
                ),
                "Unknown sender",
            )

            emails.append(
                {
                    "sender": sender,
                    "subject": subject,
                }
            )

        return emails
