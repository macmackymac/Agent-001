"""
APPA Agent Runtime

Coordinates the conversation loop between the LLM,
tool registry and providers.
"""


class AgentRuntime:

    def run(
        self,
        user_message: str,
        history: list,
        system_prompt: str,
    ):
        raise NotImplementedError(
            "Runtime not implemented yet."
        )
