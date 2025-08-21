from bson.objectid import ObjectId
from mongo import db
from models.user_model import User


collection = db['users']


def create_user(data: dict) -> str:
    user = User(**data)
    doc = user.model_dump(by_alias=True, exclude_none=True)
    result = collection.insert_one(doc)
    return str(result.inserted_id)


def get_user_by_id(user_id: str) -> dict | None:
    doc = collection.find_one({"_id": ObjectId(user_id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def list_users(query: dict | None = None) -> list[dict]:
    if query is None:
        query = {}
    items: list[dict] = []
    for doc in collection.find(query):
        doc["_id"] = str(doc["_id"])  # make JSON friendly
        items.append(doc)
    return items


def update_user(user_id: str, update_fields: dict) -> int:
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_fields})
    return result.modified_count


def delete_user(user_id: str) -> int:
    result = collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count


def add_bot_to_user(user_id: str, bot_id: str) -> int:
    result = collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$addToSet": {"bot_ids": bot_id}}  # appends safely
    )
    return result.modified_count


