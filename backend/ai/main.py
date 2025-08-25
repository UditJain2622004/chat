from typing import List
from ai.agents.prompt_verifier import prompt_verifier
from ai.agents.main_bot import main_bot
import json

def ai_reply(user_id: str, bot_id: str, chat_id: str, latest_user_messages: List[dict], chat_doc: dict) -> dict:
    # make a string of all the messages ========================================================
    messages_as_one_string = ". ".join([msg['content'] for msg in latest_user_messages])
    print("messages_as_one_string   ------ ", messages_as_one_string)

    chat_history = chat_doc['chat_history']
    # keep only "role" and "content"
    chat_history = [{"role": msg['role'], "content": msg['content']} for msg in chat_history]

    # verify the prompt ========================================================================
    res = prompt_verifier.respond(messages_as_one_string, include_chat_history=True, chat_history=chat_history)
    res = json.loads(res)
    print("verifier response   ------ ", res)
    # res['is_valid'] = False
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


    # generate the response =====================================================================
    res = main_bot.respond(messages_as_one_string, include_chat_history=True, chat_history=chat_history)
    
    return {
        "status": "success",
        "response":{
            "role": "assistant",
            "content": res
        }
    }




def dummy_ai_reply(user_id: str, bot_id: str, chat_id: str, latest_user_messages: List[dict], chat_doc: dict) -> dict:
    return {
        "status": "success",
        "response":{
            "role": "assistant",
            "content": "This is a dummy response"
        }
    }