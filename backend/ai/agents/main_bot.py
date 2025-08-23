from ai.ai import LLM
from ai.prompts.main_bot import MAIN_BOT_PROMPT


main_bot = LLM("openrouter", "grok-3-mini", system_prompt = MAIN_BOT_PROMPT)






