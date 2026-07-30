from googleapiclient.discovery import build
import streamlit as st


class GoogleServices:
    """
    Creates authenticated Google API service clients.
    """

    @staticmethod
    def gmail():
        """Return an authenticated Gmail service."""

        creds = st.session_state.get("google_credentials")

        if creds is None:
            raise Exception("Google account is not connected.")

        return build(
            "gmail",
            "v1",
            credentials=creds,
            cache_discovery=False
        )

    @staticmethod
    def drive():
        """Return an authenticated Google Drive service."""

        creds = st.session_state.get("google_credentials")

        if creds is None:
            raise Exception("Google account is not connected.")

        return build(
            "drive",
            "v3",
            credentials=creds,
            cache_discovery=False
        )
