"""
Application context shared across APPA.

The AppContext provides access to shared runtime state
without exposing Streamlit or other UI-specific objects
to the rest of the application.
"""


class AppContext:
    """
    Shared application context.
    """

    def __init__(self):
        self._google_credentials = None
        self._google_authenticated = False

    @property
    def google_credentials(self):
        return self._google_credentials

    @google_credentials.setter
    def google_credentials(self, credentials):
        self._google_credentials = credentials

    @property
    def google_authenticated(self):
        return self._google_authenticated

    @google_authenticated.setter
    def google_authenticated(self, authenticated):
        self._google_authenticated = authenticated


# Shared application context
app_context = AppContext()
