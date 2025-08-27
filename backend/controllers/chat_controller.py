from bson.objectid import ObjectId
from mongo import db
from models.chat_model import Chat, ChatMessage
from datetime import datetime
from email.utils import parsedate_to_datetime
from flask import jsonify
from controllers.utils import append_messages, get_latest_user_messages
from ai.main import ai_reply, dummy_ai_reply
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from controllers.utils import get_current_time
from controllers import user_controller, bot_controller
import re

collection = db['chats']


def create_chat(data: dict) -> str:
    # Convert any embedded messages timestamps if missing
    if 'chat_history' in data and isinstance(data['chat_history'], list) and len(data['chat_history']) > 0:
        normalized_messages = []
        for msg in data['chat_history']:
            if 'timestamp' not in msg:
                msg['timestamp'] = datetime.utcnow()
            normalized_messages.append(ChatMessage(**msg).model_dump())
        data['chat_history'] = normalized_messages

    chat = Chat(**data)
    doc = chat.model_dump(by_alias=True, exclude_none=True)
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def get_chat_by_id(chat_id: str) -> dict | None:
    doc = collection.find_one({"_id": ObjectId(chat_id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def list_chats(query: dict | None = None) -> list[dict]:
    if query is None:
        query = {}
    items: list[dict] = []
    for doc in collection.find(query):
        doc["_id"] = str(doc["_id"])  # make JSON friendly
        items.append(doc)
    return items


def update_chat(chat_id: str, update_fields: dict) -> int:
    update_fields["updated_at"] = datetime.now()
    # If updating chat_history, validate messages
    if 'chat_history' in update_fields and isinstance(update_fields['chat_history'], list):
        validated_messages = []
        for msg in update_fields['chat_history']:
            validated_messages.append(ChatMessage(**msg).model_dump())
        update_fields['chat_history'] = validated_messages

    result = collection.update_one({"_id": ObjectId(chat_id)}, {"$set": update_fields})
    return result.modified_count


def delete_chat(chat_id: str) -> int:
    result = collection.delete_one({"_id": ObjectId(chat_id)})
    return result.deleted_count


def get_chat_by_bot_and_user(bot_id: str, user_id: str) -> list[dict]:
    items: list[dict] = []
    docs = collection.find({"bot_id": bot_id, "user_id": user_id})
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # make JSON friendly
        items.append(doc)
    return items

def ensure_chat_for_pair(user_id: str, bot_id: str) -> dict:
    doc = collection.find_one({"user_id": user_id, "bot_id": bot_id})
    if doc:
        doc["_id"] = str(doc["_id"])  # normalize
        return doc
    new_chat = Chat(user_id=user_id, bot_id=bot_id, chat_history=[])
    inserted_id = collection.insert_one(new_chat.model_dump()).inserted_id
    created = collection.find_one({"_id": inserted_id})
    created["_id"] = str(created["_id"])  # normalize
    return created

def is_chat_owned_by_user(bot_id: str, user_id: str, chat_id: str) -> tuple[bool, dict]:
    doc = collection.find_one({"_id": ObjectId(chat_id), "bot_id": bot_id, "user_id": user_id})
    return doc is not None, doc if doc is not None else {}

def get_all_chat_details_by_user(user_id: str, bot_id: str, chat_id: str, remove_current_chat: bool = False) -> list[dict]:
    chat_details_docs = collection.find(
        {"user_id": user_id, "bot_id": bot_id},
        {"_id": 1, "chat_details": 1}
    )
    if remove_current_chat:
        result = [doc["chat_details"] for doc in chat_details_docs if doc["_id"] != ObjectId(chat_id)]
    else:
        result = [doc["chat_details"] for doc in chat_details_docs]

    print(f"\n\nFound {len(result)} previous chats\n\n")
    return result


def reply(data: dict) -> tuple[dict, int]:

    user_id = data.get('user_id')
    bot_id = data.get('bot_id')
    chat_id = data.get('chat_id')
    user_messages = data.get('messages', [])
    timezone = data.get('timezone')

    # print("Latest User Messages: ", user_messages)
    # print(timezone)
    # print(get_current_time(timezone))
    # return {
    #     "reply": {"role":"assistant","content":"hi"},
    # }, 200

    # =================================================================================================================
    

    if not user_id or not bot_id or not isinstance(user_messages, list) or not chat_id:
        return {"message": "Invalid or missing parameters"}, 400

    # =================================================================================================================

    # TODO: maybe remove this check if found a better way to ensure user can access only their bots
    bot_owned, chat_doc = is_chat_owned_by_user(bot_id, user_id, chat_id)
    if not bot_owned:
        return {"message": "Unauthorized"}, 403
    if not chat_doc:
        return {"message": "Bot not found"}, 404


    # get the user doc and bot doc from DB
    user_doc = user_controller.get_user_by_id(user_id)
    if not user_doc:
        return {"message": "User not found"}, 404
    bot_doc = bot_controller.get_bot_by_id(bot_id)
    if not bot_doc:
        return {"message": "Bot not found"}, 404
    all_previous_chat_details_doc = get_all_chat_details_by_user(user_id, bot_id, chat_id, remove_current_chat=True)
    print("all_previous_chat_details_doc   ------ ", all_previous_chat_details_doc)


    # =================================================================================================================

    # ai_res = dummy_ai_reply()
    ai_res = ai_reply(user_id, bot_id, chat_id, user_messages, user_doc, bot_doc, chat_doc, all_previous_chat_details_doc, verify_prompt=False)

    print("AI response :", ai_res['response']['content'])


    # =================================================================================================================
    # if AI accidentally includes <timestamp>....</timestamp> tag, remove it
    ai_res['response']['content'] = re.sub(r'<timestamp>.*?</timestamp>', '', ai_res['response']['content'])
    # add time info to ai response
    ai_res['response']['content'] = f"<timestamp>{get_current_time(timezone)}</timestamp>\n{ai_res['response']['content']}"


    # =================================================================================================================
    # append the user messages and ai reply together
    user_messages.append(ai_res['response'])
    append_messages(chat_id, user_messages)

    return {
        "reply": ai_res['response'],
    }, 200