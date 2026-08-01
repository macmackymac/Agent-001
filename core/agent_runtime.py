"""
APPA Agent Runtime

Coordinates the conversation loop between the LLM,
tool registry and providers.
"""


class AgentRuntime:

    def prepare_messages(
        self,
        user_message: str,
        history: list,
        system_prompt: str,
    ) -> list:
        """
        Build the list of messages that will be sent to the LLM.
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        messages.extend(history)

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        return messages
    
    def create_request(
        self,
        model: str,
        messages: list,
        available_tools: list | None = None,
    ) -> dict:
        """
        Build the request payload for the LLM.
        """
    
        request = {
            "model": model,
            "messages": messages,
        }
    
        if available_tools:
            request["tools"] = available_tools
    
        return request
    def execute_request(
        self,
        client,
        request: dict,
    ):
        """
        Execute a request against the active LLM provider.
        """
    
        return client.chat.completions.create(**request)
    
    def run(
        self,
        user_message: str,
        history: list,
        system_prompt: str,
    ):
        raise NotImplementedError(
            "Runtime not implemented yet."
        )
