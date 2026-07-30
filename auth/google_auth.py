import json
import streamlit as st
from google_auth_oauthlib.flow import Flow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

REDIRECT_URI = "https://agent-001-vwevvxgwtg4js5nc4c9acy.streamlit.app"


def load_client_config():
    """Load OAuth configuration from Streamlit secrets."""

    secrets = st.secrets.to_dict()
    config = secrets.get("GOOGLE_OAUTH_CREDENTIALS")

    if not config:
        raise RuntimeError("GOOGLE_OAUTH_CREDENTIALS not found.")

    if isinstance(config, str):
        config = json.loads(config)

    return config


def create_flow():
    """Create a Google OAuth flow."""

    return Flow.from_client_config(
        load_client_config(),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
def get_authorization_url():
    """
    Creates the Google authorization URL and stores the OAuth state.
    """

    flow = create_flow()

    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    st.session_state["oauth_state"] = state

    return auth_url
