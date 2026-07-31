"""
Application context shared across APPA.

The AppContext provides access to services, credentials,
and other shared resources without exposing Streamlit
or UI-specific state to the rest of the application.
"""


class AppContext:
    def __init__(self):
        self._google_credentials = None

    @property
    def google_credentials(self):
        return self._google_credentials

    @google_credentials.setter
    def google_credentials(self, credentials):
        self._google_credentials = credentials
