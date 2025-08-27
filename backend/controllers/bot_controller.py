from bson.objectid import ObjectId
from mongo import db
from models.bot_model import Bot
from controllers import user_controller, chat_controller
from datetime import datetime

collection = db['bots']
user_collection = db['users']


def create_bot(data: dict) -> str:
    bot = Bot(**data)
    doc = bot.model_dump(by_alias=True, exclude_none=True)
    result = collection.insert_one(doc)


    # create chat for the bot
    chat_id = chat_controller.create_chat({
        "user_id": data['user_id'],
        "bot_id": str(result.inserted_id),
        "chat_history": []
    })


    
    # append to bot_ids in user collection
    user_controller.add_bot_to_user(data['user_id'], bot_id=str(result.inserted_id))

    # update bot with chat_id
    # update_bot(str(result.inserted_id), {"chat_id": chat_id})


    return str(result.inserted_id)


def get_bot_by_id(bot_id: str) -> dict | None:
    doc = collection.find_one({"_id": ObjectId(bot_id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc


def list_bots(query: dict | None = None) -> list[dict]:
    if query is None:
        query = {}
    items: list[dict] = []
    for doc in collection.find(query):
        doc["_id"] = str(doc["_id"])  # make JSON friendly
        items.append(doc)
    return items


def update_bot(bot_id: str, update_fields: dict) -> int:
    update_fields["updated_at"] = datetime.now()
    result = collection.update_one({"_id": ObjectId(bot_id)}, {"$set": update_fields})
    return result.modified_count


def delete_bot(bot_id: str) -> int:
    result = collection.delete_one({"_id": ObjectId(bot_id)})
    return result.deleted_count


def get_bots_by_user_id(user_id: str) -> list[dict]:
    items: list[dict] = []
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    print(user)
    bot_ids = [ObjectId(bot_id) for bot_id in user['bot_ids']]
    print(bot_ids)  
    
    docs = collection.find({"_id": {"$in": bot_ids}})
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # make JSON friendly
        items.append(doc)
    print(items)
    return items




