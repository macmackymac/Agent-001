"""
Ollama Cloud LLM Provider

Provides an OpenAI-compatible client for Ollama Cloud.
"""

import os

import streamlit as st
from openai import OpenAI


OLLAMA_BASE_URL = "https://ollama.com/v1"
DEFAULT_MODEL = "gpt-oss:120b"


def get_ollama_api_key() -> str:
    """Retrieve the Ollama API key from environment or Streamlit secrets."""

    return (
        os.environ.get("OLLAMA_API_KEY")
        or st.secrets.get("OLLAMA_API_KEY", "")
    )


def get_ollama_model() -> str:
    """Retrieve the configured Ollama model."""

    return (
        os.environ.get("OLLAMA_MODEL")
        or st.secrets.get("OLLAMA_MODEL", DEFAULT_MODEL)
    )


def get_ollama_client():
    """Create an Ollama Cloud OpenAI-compatible client."""

    api_key = get_ollama_api_key()

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key,
        base_url=OLLAMA_BASE_URL,
    )


def is_ollama_available() -> bool:
    """Check whether Ollama is configured."""

    return bool(get_ollama_api_key())
