"""
Central registry for all APPA tools.
"""


class ToolRegistry:
    def __init__(self):
        self.tools = []
        self.implementations = {}

    def register(self, tool_definition: dict, implementation):
        """Register a tool and its implementation."""
        self.tools.append(tool_definition)
        self.implementations[
            tool_definition["function"]["name"]
        ] = implementation

    def get_tools(self):
        return self.tools

    def get_implementations(self):
        return self.implementations


registry = ToolRegistry()
