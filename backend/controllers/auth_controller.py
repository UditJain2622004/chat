from flask import Blueprint, request, jsonify, g
from middlewares.auth_middleware import token_required
from models.user_model import User
from mongo import db
from bson.objectid import ObjectId

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/sync-user', methods=['POST'])
@token_required
def sync_user():
    """
    This endpoint is called after a user signs in on the frontend.
    It receives the Firebase user info and creates/updates the user in MongoDB.
    The `token_required` decorator ensures only authenticated users can access it.
    """
    firebase_user = g.user
    user_uid = firebase_user['uid']

    # Check if user exists in our DB
    user_in_db = db.users.find_one({'uid': user_uid})

    if user_in_db:
        # User exists, convert ObjectId to string for JSON serialization
        user_in_db['_id'] = str(user_in_db['_id'])
        print("User already exists!!")
        return jsonify({"message": "User already exists.", "user": user_in_db}), 200
    else:
        # User does not exist, create a new user record
        new_user = User(
            uid=user_uid,
            email=firebase_user.get('email'),
            name=firebase_user.get('name'),
            picture=firebase_user.get('picture')
        )
        # Convert Pydantic model to dict for MongoDB insertion
        user_data = new_user.model_dump(by_alias=True, exclude_none=True)
        
        result = db.users.insert_one(user_data)
        # Add the string version of the new ObjectId to the response
        user_data['_id'] = str(result.inserted_id)

        print("User created successfully!!")
        # print(user_data)
        return jsonify({"message": "User created successfully.", "user": user_data}), 201
