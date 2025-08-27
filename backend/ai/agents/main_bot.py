from ai.ai import LLM
from ai.prompts.main_bot import MAIN_BOT_PROMPT

response_format = {
    "name": "main_bot",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "response": {"type": "string"},
            "tool_calls": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "args": {
                            "type": "object",
                            "properties": {
                                "updates": {"type": "object"}
                            },
                            "required": ["updates"],
                            "additionalProperties": False
                        }
                    },
                    "required": ["name", "args"],
                    "additionalProperties": False
                },
            },
        },

        "required": ["response"],
        "additionalProperties": False
    }
}

main_bot = LLM("openrouter", "grok-3-mini",
               system_prompt=MAIN_BOT_PROMPT, response_format=response_format)
