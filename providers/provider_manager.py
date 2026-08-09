"""
APPA LLM Provider Manager

Controls the LLM provider priority and fallback sequence:

    Ollama -> Gemini -> Groq

The manager is intentionally independent of the Streamlit UI
and the AgentRuntime.
"""

from .ollama_provider import (
    get_ollama_client,
    get_ollama_model,
    is_ollama_available,
)

from .gemini_provider import (
    get_gemini_client,
    get_gemini_model,
    is_gemini_available,
)

from .groq_provider import (
    get_groq_client,
    get_groq_model,
    is_groq_available,
)


PROVIDER_ORDER = [
    "ollama",
    "gemini",
    "groq",
]


def get_provider_client(provider: str):
    """Return the client and model for a specific provider."""

    if provider == "ollama":
        return get_ollama_client(), get_ollama_model()

    if provider == "gemini":
        return get_gemini_client(), get_gemini_model()

    if provider == "groq":
        return get_groq_client(), get_groq_model()

    raise ValueError(f"Unknown LLM provider: {provider}")


def is_provider_available(provider: str) -> bool:
    """Check whether a provider is configured."""

    if provider == "ollama":
        return is_ollama_available()

    if provider == "gemini":
        return is_gemini_available()

    if provider == "groq":
        return is_groq_available()

    return False


def get_available_providers() -> list[str]:
    """Return configured providers in priority order."""

    return [
        provider
        for provider in PROVIDER_ORDER
        if is_provider_available(provider)
    ]


def get_primary_provider():
    """Return the highest-priority configured provider."""

    for provider in PROVIDER_ORDER:
        if is_provider_available(provider):
            return provider

    return None


def get_provider_chain():
    """
    Return all configured providers in fallback order.

    Example:

        ["ollama", "gemini", "groq"]
    """

    return get_available_providers()


def get_client_and_model(provider: str):
    """
    Return (client, model) for a provider.

    Returns:
        tuple: (OpenAI client, model name)
    """

    if not is_provider_available(provider):
        return None, None

    client, model = get_provider_client(provider)

    return client, model
