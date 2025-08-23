from bson.objectid import ObjectId
from mongo import db
from models.chat_model import Chat, ChatMessage
from datetime import datetime
from email.utils import parsedate_to_datetime
from flask import jsonify
from controllers.utils import append_messages, get_latest_user_messages, is_bot_owned_by_user
from controllers.chat_details_controller import ensure_chat_details_for_pair
from ai.main import ai_reply
import time


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


def get_chat_by_bot_and_user(bot_id: str, user_id: str) -> dict | None:
    doc = collection.find_one({"bot_id": bot_id, "user_id": user_id})
    if doc:
        doc["_id"] = str(doc["_id"])  # make JSON friendly
    return doc

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


def reply(data: dict) -> tuple[dict, int]:

    user_id = data.get('user_id')
    bot_id = data.get('bot_id')
    messages = data.get('messages', [])

    # print(user_id, bot_id)

    if not user_id or not bot_id or not isinstance(messages, list):
        return {"message": "user_id, bot_id and messages are required"}, 400

    # TODO: maybe remove this check if found a better way to ensure user can access only their bots
    bot_owned, bot_doc = is_bot_owned_by_user(bot_id, user_id)
    if not bot_owned:
        return {"message": "Unauthorized"}, 403


    # chat_doc = ensure_chat_for_pair(user_id, bot_id)
    # ensure_chat_details_for_pair(user_id, bot_id, chat_doc['_id'])


    # Determine only the new user messages to append: slice after last assistant
    new_user_messages = get_latest_user_messages(messages)
    print(new_user_messages)


    # TODO: maybe append the user messages and ai reply together instead of separately to save a db call
    if new_user_messages:
        append_messages(bot_doc['chat_id'], new_user_messages)

    ai_res = ai_reply(user_id, bot_id, bot_doc['chat_id'], new_user_messages)

    # if ai_res['status'] == 'failed':
    #     return {"message": ai_res['failure_reason']}, 400

    # print(ai_res)
    append_messages(bot_doc['chat_id'], [ai_res['response']])

    # final_chat = get_chat_by_id(chat_doc['_id'])
    time.sleep(3)
    return {
        # "chat": final_chat,
        "reply": ai_res['response'],
    }, 200