"""
Provider Manager
Handles AI provider selection and fallback.
"""

import os

import streamlit as st
from openai import OpenAI

from core.config import (
    DEFAULT_PROVIDER,
    GEMINI_MODEL,
    GROQ_MODEL,
)


class ProviderManager:

    def __init__(self):

        if "provider" not in st.session_state:
            st.session_state.provider = DEFAULT_PROVIDER

        if "switched_to_groq" not in st.session_state:
            st.session_state.switched_to_groq = False

    def current_provider(self):

        return st.session_state.provider

    def gemini_client(self):

        api_key = (
            os.environ.get("GEMINI_API_KEY")
            or st.secrets.get("GEMINI_API_KEY", "")
        )

        if not api_key:
            return None

        return OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

    def groq_client(self):

        api_key = (
            os.environ.get("GROQ_API_KEY")
            or st.secrets.get("GROQ_API_KEY", "")
        )

        if not api_key:
            return None

        return OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    def get(self):

        if st.session_state.provider == "gemini":

            client = self.gemini_client()

            if client:
                return client, GEMINI_MODEL

        client = self.groq_client()

        if client:
            return client, GROQ_MODEL

        return None, None

    def switch_to_groq(self):

        st.session_state.provider = "groq"
        st.session_state.switched_to_groq = True

    def reset(self):

        st.session_state.provider = DEFAULT_PROVIDER
        st.session_state.switched_to_groq = False
