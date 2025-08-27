from bson.objectid import ObjectId
from datetime import datetime
from typing import Any, Dict


from mongo import db


collection = db["users"]


def get_user_details(user_id: str) -> dict | None:
    doc = collection.find_one({"_id": ObjectId(user_id)}, {"user_details": 1})
    if not doc:
        return None
    return doc.get("user_details") or {}


def clear_user_details(user_id: str) -> int:
    from models.user_model import UserDetails  # Assuming your Pydantic models are in models.py

    empty_user_details = UserDetails()
    empty_user_details.updated_at = datetime.now()
    result = collection_users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"user_details": empty_user_details.dict()}}
    )
    return result.modified_count

def update_user_details(user_id: str, updates: Dict[str, Any]) -> int:
    """
    Update fields in user_details:
    - String fields: nickname, available_timings
    - List field: anything_else supports add/remove
    - Dict fields (future-proof): supports set/remove
    - 'name' cannot be updated

    Example updates:
        {
            "nickname": "buddy",
            "anything_else": {"add": ["note1"], "remove": ["note2"]},
            "some_dict_field": {"set": {"key1": "val"}, "remove": ["old_key"]}
        }
    """
    set_ops = {}
    unset_ops = {}
    add_to_set_ops = {}
    pull_all_ops = {}

    allowed_string_fields = {"nickname", "available_timings"}
    allowed_list_fields = {"anything_else", "preferences", "dislikes", "task_following_record"}

    for field, value in updates.items():
        # --- String fields ---
        if field in allowed_string_fields:
            if not isinstance(value, str):
                raise ValueError(f"Field '{field}' must be a string")
            set_ops[f"user_details.{field}"] = value

        # --- List fields ---
        elif field in allowed_list_fields:
            if not isinstance(value, dict):
                raise ValueError(f"Field '{field}' must be a dict with 'add'/'remove'")
            if "add" in value:
                vals = value["add"]
                if not isinstance(vals, list):
                    vals = [vals]
                add_to_set_ops[f"user_details.{field}"] = {"$each": vals}
            if "remove" in value:
                vals = value["remove"]
                if not isinstance(vals, list):
                    vals = [vals]
                pull_all_ops[f"user_details.{field}"] = vals

        # --- Dict fields (future-proof) ---
        elif isinstance(value, dict) and ("set" in value or "remove" in value):
            # set keys
            if "set" in value:
                for k, v in value["set"].items():
                    set_ops[f"user_details.{field}.{k}"] = v
            # remove keys
            if "remove" in value:
                keys_to_remove = value["remove"]
                if not isinstance(keys_to_remove, list):
                    keys_to_remove = [keys_to_remove]
                for k in keys_to_remove:
                    unset_ops[f"user_details.{field}.{k}"] = ""



    # Always update updated_at
    set_ops["updated_at"] = datetime.now()

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

    result = collection.update_one({"_id": ObjectId(user_id)}, update_doc)
    return result.modified_count