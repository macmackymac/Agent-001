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
from tools.gmail_tools import read_recent_emails
from tools.drive_tools import save_to_google_drive
from tools.calendar_tools import get_calendar_events

def initialize_tools():
    """
    Register every tool available to APPA.
    """
    pass
