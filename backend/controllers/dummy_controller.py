"""
controllers/dummy_controller.py: Implements CRUD operations for Dummy model
"""


from mongo import db
from bson.objectid import ObjectId
from models.dummy_model import DummyModel

collection = db['dummy']

def create_dummy(name, age):
    # Validate input using Pydantic
    dummy = DummyModel(name=name, age=age)
    doc = dummy.model_dump()
    result = collection.insert_one(doc)
    return str(result.inserted_id)

def read_dummy(query=None):
    if query is None:
        query = {}
    return list(collection.find(query))

def update_dummy(dummy_id, update_fields):
    result = collection.update_one({"_id": ObjectId(dummy_id)}, {"$set": update_fields})
    return result.modified_count

def delete_dummy(dummy_id):
    result = collection.delete_one({"_id": ObjectId(dummy_id)})
    return result.deleted_count
