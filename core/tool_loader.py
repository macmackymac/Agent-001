"""
Registers all tools available to APPA.
"""

from core.tool_registry import registry

# Core tools
from core.tools import (
    calculate,
    get_current_time,
    search_web,
    remember_information,
)

# Google Workspace tools
from streamlit_app import (
    read_recent_emails,
    save_to_google_drive,
    get_calendar_events,
)


def initialize_tools():
    """
    Register every tool available to APPA.
    """
    pass
