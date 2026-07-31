from datetime import datetime, timedelta

from googleapiclient.discovery import build


class CalendarService:
    def __init__(self, credentials):
        self.service = build(
            "calendar",
            "v3",
            credentials=credentials,
        )

    def get_upcoming_events(self, max_results=10):

        now = datetime.utcnow().isoformat() + "Z"

        events = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return events.get("items", [])
