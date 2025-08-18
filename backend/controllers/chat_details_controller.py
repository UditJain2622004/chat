from bson.objectid import ObjectId
from mongo import db
from models.chat_details import ChatDetails


collection = db['chat_details']


def create_chat_details(data: dict) -> str:
    chat_details = ChatDetails(**data)
    doc = chat_details.model_dump(by_alias=True, exclude_none=True)
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def get_chat_details_by_id(details_id: str) -> dict | None:
    doc = collection.find_one({"_id": ObjectId(details_id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def list_chat_details(query: dict | None = None) -> list[dict]:
    if query is None:
        query = {}
    items: list[dict] = []
    for doc in collection.find(query):
        doc["_id"] = str(doc["_id"])  # make JSON friendly
        items.append(doc)
    return items


def update_chat_details(details_id: str, update_fields: dict) -> int:
    result = collection.update_one({"_id": ObjectId(details_id)}, {"$set": update_fields})
    return result.modified_count


def delete_chat_details(details_id: str) -> int:
    result = collection.delete_one({"_id": ObjectId(details_id)})
    return result.deleted_count


def get_chat_details(user_id: str, bot_id: str, chat_id: str) -> dict | None:
    doc = collection.find_one({
        "user_id": user_id,
        "bot_id": bot_id,
        "chat_id": chat_id,
    })
    if doc:
        doc["_id"] = str(doc["_id"])  # make JSON friendly
    return doc


def ensure_chat_details_for_pair(user_id: str, bot_id: str, chat_id: str) -> dict:
    doc = get_chat_details(user_id, bot_id, chat_id)
    if doc:
        return doc
    details = ChatDetails(
        user_id=user_id,
        bot_id=bot_id,
        chat_id=chat_id,
        rules=[],
        current_mood="dominant",
        important_events=[],
        nickname=None,
        any_other_such_details={},
    )
    inserted_id = collection.insert_one(details.model_dump()).inserted_id
    created = collection.find_one({"_id": inserted_id})
    created["_id"] = str(created["_id"])  # normalize
    return created

