"""
APPA Configuration
Central location for application constants and settings.
"""

APP_NAME = "APPA"
APP_ICON = "🤖"

# ---------- LLM ----------

DEFAULT_PROVIDER = "gemini"

GEMINI_MODEL = "gemini-2.5-flash"

GROQ_MODEL = "openai/gpt-oss-20b"

# ---------- Google OAuth ----------

GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

REDIRECT_URI = (
    "https://agent-001-vwevvxgwtg4js5nc4c9acy.streamlit.app"
)

# ---------- Agent ----------

MAX_STEPS = 8

MAX_TOOL_FAILURES = 2

TOOL_ERROR = "TOOL_ERROR:"
