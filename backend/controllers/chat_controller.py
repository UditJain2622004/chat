from bson.objectid import ObjectId
from mongo import db
from models.chat_model import Chat, ChatMessage
from datetime import datetime
from email.utils import parsedate_to_datetime


collection = db['chats']


def create_chat(data: dict) -> str:
    # Convert any embedded messages timestamps if missing
    if 'chat_history' in data and isinstance(data['chat_history'], list):
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


def append_messages(chat_id: str, messages: list[dict]) -> int:
    validated = []
    for msg in messages:
        # normalize timestamp
        ts = msg.get("timestamp")
        if isinstance(ts, datetime):
            pass
        elif isinstance(ts, str):
            parsed = None
            # try RFC2822/HTTP-date
            try:
                parsed = parsedate_to_datetime(ts)
            except Exception:
                parsed = None
            # try ISO format
            if parsed is None:
                try:
                    parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except Exception:
                    parsed = None
            msg["timestamp"] = parsed or datetime.utcnow()
        else:
            msg["timestamp"] = datetime.utcnow()

        validated.append(ChatMessage(**msg).model_dump())
    res = collection.update_one({"_id": ObjectId(chat_id)}, {"$push": {"chat_history": {"$each": validated}}})
    return res.modified_count

