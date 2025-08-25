from bson.objectid import ObjectId
from datetime import datetime
from typing import Any, Dict


from mongo import db


collection = db["chats"]


def get_chat_details(chat_id: str) -> dict | None:
    doc = collection.find_one({"_id": ObjectId(chat_id)}, {"chat_details": 1})
    if not doc:
        return None
    return doc.get("chat_details") or {}

def clear_chat_details(chat_id: str) -> int:
    from models.chat_model import ChatDetails  # Assuming your Pydantic models are in models.py

    empty_chat_details = ChatDetails()  # default object
    empty_chat_details.updated_at = datetime.now()

    result = collection_chats.update_one(
        {"_id": ObjectId(chat_id)},
        {"$set": {"chat_details": empty_chat_details.dict()}}
    )
    return result.modified_count

def update_chat_details(chat_id: str, updates: Dict[str, Any]) -> int:
    """
    Mongo-native update compatible with the LLM tool schema:
    - Strings: {"current_mood": "happy"}
    - Lists: {"rules": {"add": [...], "remove": [...]}}
    - Dicts: {"any_other_such_details": {"set": {...}, "remove": [...]}}
    """
    set_ops = {}
    unset_ops = {}
    add_to_set_ops = {}
    pull_all_ops = {}

    # Strings and primitives
    for field, value in updates.items():
        if field in ["current_mood", "nickname"]:
            set_ops[f"chat_details.{field}"] = value

        # Lists
        elif field in ["rules", "important_events"]:
            lst_ops = updates[field]
            if "add" in lst_ops:
                vals = lst_ops["add"]
                if not isinstance(vals, list):
                    vals = [vals]
                add_to_set_ops[f"chat_details.{field}"] = {"$each": vals}
            if "remove" in lst_ops:
                vals = lst_ops["remove"]
                if not isinstance(vals, list):
                    vals = [vals]
                pull_all_ops[f"chat_details.{field}"] = vals

        # Dicts
        elif field == "any_other_such_details":
            dict_ops = updates[field]
            if "set" in dict_ops:
                for k, v in dict_ops["set"].items():
                    set_ops[f"chat_details.any_other_such_details.{k}"] = v
            if "remove" in dict_ops:
                keys_to_remove = dict_ops["remove"]
                if not isinstance(keys_to_remove, list):
                    keys_to_remove = [keys_to_remove]
                for k in keys_to_remove:
                    unset_ops[f"chat_details.any_other_such_details.{k}"] = ""

    # Always update updated_at
    set_ops["chat_details.updated_at"] = datetime.now()

    update_doc = {}
    if set_ops:
        update_doc["$set"] = set_ops
    if unset_ops:
        update_doc["$unset"] = unset_ops
    if add_to_set_ops:
        update_doc["$addToSet"] = add_to_set_ops
    if pull_all_ops:
        update_doc["$pullAll"] = pull_all_ops

    if not update_doc:
        return 0

    result = collection.update_one({"_id": ObjectId(chat_id)}, update_doc)
    return result.modified_count