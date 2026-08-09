"""
Groq LLM Provider

Provides an OpenAI-compatible client for Groq.
"""

import os

import streamlit as st
from openai import OpenAI


GROQ_BASE_URL = "https://api.groq.com/openai/v1"

DEFAULT_MODEL = "openai/gpt-oss-20b"


def get_groq_api_key() -> str:
    """Retrieve the Groq API key from environment or Streamlit secrets."""

    return (
        os.environ.get("GROQ_API_KEY")
        or st.secrets.get("GROQ_API_KEY", "")
    )


def get_groq_model() -> str:
    """Retrieve the configured Groq model."""

    return (
        os.environ.get("GROQ_MODEL")
        or st.secrets.get("GROQ_MODEL", DEFAULT_MODEL)
    )


def get_groq_client():
    """Create a Groq OpenAI-compatible client."""

    api_key = get_groq_api_key()

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key,
        base_url=GROQ_BASE_URL,
    )


def is_groq_available() -> bool:
    """Check whether Groq is configured."""

    return bool(get_groq_api_key())
