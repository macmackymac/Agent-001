import streamlit as st

from core.config import DEFAULT_PROVIDER


class SessionManager:

    @staticmethod
    def initialize():

        defaults = {
            "messages": [],
            "provider": DEFAULT_PROVIDER,
            "switched_to_groq": False,
            "google_authenticated": False,
            "google_credentials": None,
            "oauth_state": None,
        }

        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @staticmethod
    def clear_chat():

        st.session_state.messages = []
        st.session_state.provider = DEFAULT_PROVIDER
        st.session_state.switched_to_groq = False
