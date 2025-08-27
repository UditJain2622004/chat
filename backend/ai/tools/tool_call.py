from ai.tools.chat_details_controller import update_chat_details
from ai.tools.user_details_controller import update_user_details

def call_tools(user_id: str, bot_id: str, chat_id: str, tool_calls: list):
    for tool_call in tool_calls:

        if tool_call['name'] == 'update_user_details':
            print("Updating User Details ------ ", tool_call['args']['updates'])
            update_user_details(user_id, tool_call['args']['updates'])
        elif tool_call['name'] == 'update_chat_details':
            print("Updating Chat Details ------ ", tool_call['args']['updates'])
            update_chat_details(chat_id, tool_call['args']['updates'])


