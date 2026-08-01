"""
Registers all tools available to APPA.
"""

from core.tool_registry import registry
from tools.tool_definitions import TOOLS

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

    implementations = {
        "calculate": calculate,
        "get_current_time": get_current_time,
        "search_web": search_web,
        "read_recent_emails": read_recent_emails,
        "save_to_google_drive": save_to_google_drive,
        "get_calendar_events": get_calendar_events,
        "remember_information": remember_information,
    }

    for tool in TOOLS:
        name = tool["function"]["name"]

        implementation = implementations.get(name)

        if implementation is not None:
            registry.register(tool, implementation)
