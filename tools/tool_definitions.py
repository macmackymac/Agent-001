"""
Central tool definitions for APPA.

This module contains only the OpenAI-compatible
tool schemas.

No implementations belong here.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a numeric arithmetic expression exactly.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "An arithmetic expression, e.g. '1450 * 0.12'.",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time in a given timezone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "IANA timezone name, e.g. 'Asia/Manila'. Defaults to UTC.",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": (
                "Search the web and return titles, URLs and short snippets. "
                "Use for current events, recent figures, or any fact you are "
                "not confident about. Snippets are brief. Do not call this more "
                "than three times for one question."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search terms, e.g. 'Metro Manila population 2026'.",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "How many results to return, 1-8. Defaults to 5.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_recent_emails",
            "description": "Read unread emails from Gmail inbox.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Number of emails to fetch, 1-10. Defaults to 5.",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_to_google_drive",
            "description": "Save a file or content to Google Drive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file to save, e.g. 'notes.txt'.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The file content to save.",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_calendar_events",
            "description": "Read upcoming Google Calendar events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remember_information",
            "description": "Remember important long-term information about the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "Memory key"
                    },
                    "value": {
                        "type": "string",
                        "description": "Memory value"
                    }
                },
                "required": [
                    "key",
                    "value"
                ]
            }
        }
    },
]
