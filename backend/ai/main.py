from typing import List
from ai.agents.prompt_verifier import prompt_verifier
from ai.agents.main_bot import main_bot
import json

def ai_reply(user_id: str, bot_id: str, chat_id: str, last_user_messages: List[dict]) -> dict:
    # make a string of all the messages
    messages_as_one_string = ". ".join([msg['content'] for msg in last_user_messages])
    print("messages_as_one_string   ------ ", messages_as_one_string)
    # verify the prompt
    res = prompt_verifier.respond(messages_as_one_string)
    res = json.loads(res)
    print("verifier response   ------ ", res)
    if not res['is_valid']:
        return {
            "status": "failed",
            "failure_reason": "Prompt Verification Failed",
            "failure_details": res['reason'],
            "response":{
                "role": "assistant",
                "content": res['reason']
            }
        }

    # generate the response
    res = main_bot.respond(messages_as_one_string)
    
    return {
        "status": "success",
        "response":{
            "role": "assistant",
            "content": res
        }
        
    }