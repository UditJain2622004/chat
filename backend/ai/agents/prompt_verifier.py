from ai.ai import LLM
from ai.prompts.prompt_verifier import PROMPT_VERIFIER_PROMPT
from dotenv import load_dotenv

load_dotenv()

response_format = {
    "name": "prompt_verifier",
    "strict":True,
    "schema": {
        "type": "object",
        "properties": {
            "is_valid": {"type": "boolean"},
            "reason": {"type": "string"},
        },
    },
    "required": ["is_valid", "reason"],
    "additionalProperties": False
}

prompt_verifier = LLM("openrouter", "grok-3-mini", system_prompt = PROMPT_VERIFIER_PROMPT, response_format = response_format)

# def verify_prompt(prompt: str) -> dict:
#     res = prompt_verifier.generate_response(prompt)
#     return res

# res = prompt_verifier.generate_response("What is the capital of France?")
# print(res)






