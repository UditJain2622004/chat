from flask import Blueprint, request, jsonify
from controllers.chat_details_controller import (
    create_chat_details,
    get_chat_details_by_id,
    list_chat_details,
    update_chat_details,
    delete_chat_details,
    get_chat_details,
)


chat_details_bp = Blueprint('chat_details', __name__)


@chat_details_bp.route('/', methods=['POST'])
def route_create_chat_details():
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400
    inserted_id = create_chat_details(data)
    return jsonify({"_id": inserted_id}), 201


@chat_details_bp.route('/', methods=['GET'])
def route_list_chat_details():
    user_id = request.args.get('user_id')
    bot_id = request.args.get('bot_id')
    chat_id = request.args.get('chat_id')
    if user_id and bot_id and chat_id:
        details = get_chat_details(user_id, bot_id, chat_id)
        if not details:
            return jsonify({"message": "Chat details not found"}), 404
        return jsonify(details), 200
    details = list_chat_details()
    return jsonify(details), 200


@chat_details_bp.route('/<details_id>', methods=['GET'])
def route_get_chat_details_by_id(details_id: str):
    details = get_chat_details_by_id(details_id)
    if not details:
        return jsonify({"message": "Chat details not found"}), 404
    return jsonify(details), 200


@chat_details_bp.route('/<details_id>', methods=['PUT', 'PATCH'])
def route_update_chat_details(details_id: str):
    update_fields = request.get_json(silent=True) or {}
    modified = update_chat_details(details_id, update_fields)
    if modified == 0:
        return jsonify({"message": "No changes or chat details not found"}), 404
    return jsonify({"modified": modified}), 200


@chat_details_bp.route('/<details_id>', methods=['DELETE'])
def route_delete_chat_details(details_id: str):
    deleted = delete_chat_details(details_id)
    if deleted == 0:
        return jsonify({"message": "Chat details not found"}), 404
    return jsonify({"deleted": deleted}), 200


