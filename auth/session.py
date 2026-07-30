import streamlit as st


def initialize_session():
    """
    Initialize all session state variables used by the application.
    Safe to call multiple times.
    """

    defaults = {
        "google_authenticated": False,
        "google_credentials": None,
        "provider": "gemini",
        "switched_to_groq": False,
        "messages": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_google_session():
    """Disconnect Google and clear stored credentials."""

    st.session_state.google_authenticated = False
    st.session_state.google_credentials = None


def is_google_authenticated():
    """Return True if Google is connected."""

    return (
        st.session_state.google_authenticated
        and st.session_state.google_credentials is not None
    )
