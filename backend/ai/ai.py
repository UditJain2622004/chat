from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()  # Loads .env into environment variables

llm_id_map = {
    "openrouter":{
        "grok-3-mini": "x-ai/grok-3-mini",
        "grok-3": "x-ai/grok-3",
        "grok-4": "x-ai/grok-4"
    }
}

def format_message(message, role):
    return {
        "role": role,
        "content": message,
    }


class LLM:
    def __init__(self, provider, model_name, system_prompt = "You are a helpful assistant.", chat_history = []):
        self.provider = provider
        if provider in llm_id_map:
            self.model_name = llm_id_map[provider].get(model_name, model_name)
        else:
            self.model_name = model_name

        self.system_prompt = system_prompt
        self.chat_history = chat_history

    def chat_response(self, user_message):
        self.chat_history.append({"role": "user", "content": user_message})
        response = self.generate_response(user_message, chat_history=True)
        self.chat_history.append({"role": "assistant", "content": response})
        return response

    def generate_response(self, user_message, chat_history=False):
        if self.provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            messages = [{"role":"developer", "content": self.system_prompt}]
            if chat_history:
                messages.extend(self.chat_history)
            else:
                messages.append(format_message(user_message, "user"))

            # print(messages)
            completion = client.chat.completions.create(
                # extra_headers={
                #     "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                #     "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
                # },
                extra_body={
                    "reasoning_effort": "low"
                },
                model=self.model_name,
                messages=messages
            )

            # print(completion)
            # print(completion.choices[0].message.content)
            # print(completion.choices[0].message.reasoning_details[0].get("text"))

            if completion.choices:
                return completion.choices[0].message.content
            return "No response"

        else:
            raise ValueError("Unsupported provider!")