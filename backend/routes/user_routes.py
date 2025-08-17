from flask import Blueprint, request, jsonify
from controllers.user_controller import (
    create_user,
    get_user_by_id,
    list_users,
    update_user,
    delete_user,
)


users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['POST'])
def route_create_user():
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400
    inserted_id = create_user(data)
    return jsonify({"_id": inserted_id}), 201


@users_bp.route('/', methods=['GET'])
def route_list_users():
    users = list_users()
    return jsonify(users), 200


@users_bp.route('/<user_id>', methods=['GET'])
def route_get_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user), 200


@users_bp.route('/<user_id>', methods=['PUT', 'PATCH'])
def route_update_user(user_id: str):
    update_fields = request.get_json(silent=True) or {}
    modified = update_user(user_id, update_fields)
    if modified == 0:
        return jsonify({"message": "No changes or user not found"}), 404
    return jsonify({"modified": modified}), 200


@users_bp.route('/<user_id>', methods=['DELETE'])
def route_delete_user(user_id: str):
    deleted = delete_user(user_id)
    if deleted == 0:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"deleted": deleted}), 200


