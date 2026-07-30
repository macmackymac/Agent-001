import json
import streamlit as st

from google_auth_oauthlib.flow import Flow


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

REDIRECT_URI = "https://agent-001-vwevvxgwtg4js5nc4c9acy.streamlit.app"


class GoogleAuth:

    @staticmethod
    def create_flow():
        secrets = st.secrets.to_dict()

        config = secrets.get("GOOGLE_OAUTH_CREDENTIALS")

        if not config:
            raise Exception("GOOGLE_OAUTH_CREDENTIALS missing.")

        if isinstance(config, str):
            config = json.loads(config)

        return Flow.from_client_config(
            config,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,
        )

    @staticmethod
    def authorization_url():

        flow = GoogleAuth.create_flow()

        auth_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )

        st.session_state.oauth_state = state

        return auth_url

    @staticmethod
    def exchange_code(code):

        flow = GoogleAuth.create_flow()

        flow.fetch_token(code=code)

        creds = flow.credentials

        st.session_state.google_credentials = creds
        st.session_state.google_authenticated = True

        return creds
