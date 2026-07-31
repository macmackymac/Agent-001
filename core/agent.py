"""
APPA Agent Engine
Coordinates the conversation loop between the LLM and registered tools.
"""

from core.provider import ProviderManager
from core.tool_registry import registry
from core.agent_runtime import AgentRuntime

class Agent:

    def __init__(self):
        self.provider = ProviderManager()

    def available_tools(self):
        """Return registered tool definitions."""
        return registry.get_tools()

    def tool_implementations(self):
        """Return registered tool implementations."""
        return registry.get_implementations()
