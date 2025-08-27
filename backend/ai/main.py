from typing import List
from ai.agents.prompt_verifier import prompt_verifier
from ai.agents.main_bot import main_bot
import json
from ai.prompts.main_bot import MAIN_BOT_PROMPT
from ai.tools.tool_call import call_tools

def ai_reply(user_id: str, bot_id: str, chat_id: str, latest_user_messages: List[dict], user_doc: dict, bot_doc: dict, chat_doc: dict, all_previous_chat_details_doc: List[dict], verify_prompt: bool = True) -> dict:

    chat_details = chat_doc.get('chat_details', {})
    user_details = user_doc.get('user_details', {})
    bot_details = bot_doc.get('bot_details', {})
    SYSTEM_PROMPT = MAIN_BOT_PROMPT
    # print("bot_details   ------ ", bot_doc)

    # return {
    #     "status": "success",
    #     "response":{
    #         "role": "assistant",
    #         "content": "<msg>This is a dummy response</msg>"
    #     }
    # }

    # message transformation ============================================================================
    messages_as_one_string = ". ".join([msg['content'] for msg in latest_user_messages])

    transformed_message = f"""
    <user_details>{json.dumps(user_details, default=str)}</user_details>
    <your_details>{json.dumps(bot_details, default=str)}</your_details>
    <important_details_about_current_chat>{json.dumps(chat_details, default=str)}</important_details_about_current_chat>
    {messages_as_one_string}
    """
    print("transformed_message   ------ ", transformed_message)

    # system prompt transformation ============================================================================
    SYSTEM_PROMPT += f"<all_previous_chat_details>{json.dumps(all_previous_chat_details_doc, default=str)}</all_previous_chat_details>"


    # ==================================================================================================
    chat_history = chat_doc['chat_history']
    # keep only "role" and "content"
    chat_history = [{"role": msg['role'], "content": msg['content']} for msg in chat_history]

    # verify the prompt =========================================================================
    if verify_prompt:
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
                    "content": f"<msg>{res['reason']}</msg>"
                }
            }


    # generate the response =====================================================================
    res = main_bot.respond(transformed_message, system_prompt= SYSTEM_PROMPT, include_chat_history=True, chat_history=chat_history)
    json_res = json.loads(res)
    print("json_res   ------ ", json_res)
    if json_res.get('tool_calls', None):
        print("Calling Tools ---------")
        call_tools(user_id, bot_id, chat_id, json_res['tool_calls'])
    
    
    return {
        "status": "success",
        "response":{
            "role": "assistant",
            "content": json_res['response']
        }
    }




def dummy_ai_reply() -> dict:
    return {
        "status": "success",
        "response":{
            "role": "assistant",
            "content": "<msg>This is a dummy response</msg>"
        }
    }