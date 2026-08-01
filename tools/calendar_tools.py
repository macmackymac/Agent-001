"""
Google Calendar tool functions for APPA.
"""

from services.calendar_service import CalendarService

TOOL_ERROR = "TOOL_ERROR:"


def get_calendar_events(
    google_authenticated,
    google_credentials,
    max_results: int = 10,
) -> str:
    """
    Read upcoming Google Calendar events.
    """

    if not google_authenticated or not google_credentials:
        return (
            f"{TOOL_ERROR} Google Calendar not authenticated. "
            "Connect in the sidebar first."
        )

    try:
        calendar = CalendarService(
            google_credentials
        )

        events = calendar.get_upcoming_events(max_results)

        if not events:
            return "No upcoming events."

        output = []

        for event in events:

            start = event["start"].get(
                "dateTime",
                event["start"].get("date")
            )

            title = event.get(
                "summary",
                "(No Title)"
            )

            output.append(
                f"{start}\n{title}"
            )

        return "\n\n".join(output)

    except Exception as exc:
        return f"{TOOL_ERROR} {exc}"
