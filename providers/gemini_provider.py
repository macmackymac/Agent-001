"""
Gemini LLM Provider

Provides an OpenAI-compatible client for Google Gemini.
"""

import os

import streamlit as st
from openai import OpenAI


GEMINI_BASE_URL = (
    "https://generativelanguage.googleapis.com/v1beta/openai/"
)

DEFAULT_MODEL = "gemini-3-flash-preview"


def get_gemini_api_key() -> str:
    """Retrieve the Gemini API key from environment or Streamlit secrets."""

    return (
        os.environ.get("GEMINI_API_KEY")
        or st.secrets.get("GEMINI_API_KEY", "")
    )


def get_gemini_model() -> str:
    """Retrieve the configured Gemini model."""

    return (
        os.environ.get("GEMINI_MODEL")
        or st.secrets.get("GEMINI_MODEL", DEFAULT_MODEL)
    )


def get_gemini_client():
    """Create a Gemini OpenAI-compatible client."""

    api_key = get_gemini_api_key()

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key,
        base_url=GEMINI_BASE_URL,
    )


def is_gemini_available() -> bool:
    """Check whether Gemini is configured."""

    return bool(get_gemini_api_key())
