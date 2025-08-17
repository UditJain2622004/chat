from flask import Blueprint, request, jsonify
from controllers.chat_controller import (
    create_chat,
    get_chat_by_id,
    list_chats,
    update_chat,
    delete_chat,
    get_chat_by_bot_and_user,
)


chats_bp = Blueprint('chats', __name__)


@chats_bp.route('/', methods=['POST'])
def route_create_chat():
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400
    inserted_id = create_chat(data)
    return jsonify({"_id": inserted_id}), 201


@chats_bp.route('/', methods=['GET'])
def route_list_chats():
    bot_id = request.args.get('bot_id')
    user_id = request.args.get('user_id')
    if bot_id and user_id:
        chat = get_chat_by_bot_and_user(bot_id, user_id)
        if not chat:
            return jsonify({"message": "Chat not found"}), 404
        return jsonify(chat), 200
    chats = list_chats()
    return jsonify(chats), 200


@chats_bp.route('/<chat_id>', methods=['GET'])
def route_get_chat(chat_id: str):
    chat = get_chat_by_id(chat_id)
    if not chat:
        return jsonify({"message": "Chat not found"}), 404
    return jsonify(chat), 200


@chats_bp.route('/<chat_id>', methods=['PUT', 'PATCH'])
def route_update_chat(chat_id: str):
    update_fields = request.get_json(silent=True) or {}
    modified = update_chat(chat_id, update_fields)
    if modified == 0:
        return jsonify({"message": "No changes or chat not found"}), 404
    return jsonify({"modified": modified}), 200


@chats_bp.route('/<chat_id>', methods=['DELETE'])
def route_delete_chat(chat_id: str):
    deleted = delete_chat(chat_id)
    if deleted == 0:
        return jsonify({"message": "Chat not found"}), 404
    return jsonify({"deleted": deleted}), 200


