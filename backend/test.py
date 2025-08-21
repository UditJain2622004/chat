from openai import OpenAI
from dotenv import load_dotenv
import os

from ai.ai import LLM

load_dotenv()  # Loads .env into environment variables

api_key = os.getenv("OPENROUTER_API_KEY")

# llm = LLM("openrouter", "grok-3-mini", system_prompt="Answer in 1 word, don't think at all, just respond.")

chatHistory = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "user", "content": "and of Pakistan?"},
    # {"role": "user", "content": "also, who won the 2011 ODI cricket world cup?"},
]

# llm = LLM("openrouter", "grok-3-mini", chat_history = chatHistory)

# res = llm.chat_response("also, who won the 2011 ODI cricket world cup?")
# print(res)




# res = llm.generate_response("What is the capital of France?")
# print(res)

# res = llm.chat_response("What is the capital of Pakistan?")
# print(res)


a = ""

if a:
    print("Yes")
else:
    print("NO")
