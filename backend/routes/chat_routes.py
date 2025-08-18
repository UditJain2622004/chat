from flask import Blueprint, request, jsonify
from controllers.chat_controller import (
    create_chat,
    get_chat_by_id,
    list_chats,
    update_chat,
    delete_chat,
    get_chat_by_bot_and_user,
    ensure_chat_for_pair,
    append_messages,
)
from controllers.chat_details_controller import ensure_chat_details_for_pair
from controllers.bot_controller import is_bot_owned_by_user
from flask import request


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


@chats_bp.route('/id/<chat_id>', methods=['GET'])
def route_get_chat(chat_id: str):
    chat = get_chat_by_id(chat_id)
    if not chat:
        return jsonify({"message": "Chat not found"}), 404
    return jsonify(chat), 200


@chats_bp.route('/id/<chat_id>', methods=['PUT', 'PATCH'])
def route_update_chat(chat_id: str):
    update_fields = request.get_json(silent=True) or {}
    modified = update_chat(chat_id, update_fields)
    if modified == 0:
        return jsonify({"message": "No changes or chat not found"}), 404
    return jsonify({"modified": modified}), 200


@chats_bp.route('/id/<chat_id>', methods=['DELETE'])
def route_delete_chat(chat_id: str):
    deleted = delete_chat(chat_id)
    if deleted == 0:
        return jsonify({"message": "Chat not found"}), 404
    return jsonify({"deleted": deleted}), 200


@chats_bp.route('/send', methods=['POST'])
def route_send_message():
    """
    Body: { user_id, bot_id, messages: [{role, content, timestamp?}, ...] }
    Ensures chat + chat_details exist, verifies ownership, appends messages, returns dummy reply.
    """
    data = request.get_json(silent=True) or {}
    user_id = data.get('user_id')
    bot_id = data.get('bot_id')
    messages = data.get('messages', [])

    if not user_id or not bot_id or not isinstance(messages, list):
        return jsonify({"message": "user_id, bot_id and messages are required"}), 400

    if not is_bot_owned_by_user(bot_id, user_id):
        return jsonify({"message": "Bot does not belong to user"}), 403

    chat_doc = ensure_chat_for_pair(user_id, bot_id)
    ensure_chat_details_for_pair(user_id, bot_id, chat_doc['_id'])

    # Determine only the new user messages to append: slice after last assistant
    last_assistant_index = -1
    for idx in range(len(messages) - 1, -1, -1):
        try:
            if isinstance(messages[idx], dict) and messages[idx].get('role') == 'assistant':
                last_assistant_index = idx
                break
        except Exception:
            continue

    pending = messages[last_assistant_index + 1:] if last_assistant_index >= 0 else messages
    new_user_messages = [m for m in pending if isinstance(m, dict) and m.get('role') == 'user']

    if new_user_messages:
        append_messages(chat_doc['_id'], new_user_messages)

    dummy_reply = {
        "role": "assistant",
        "content": "This is a dummy AI response. (Hook up your AI here.)"
    }
    append_messages(chat_doc['_id'], [dummy_reply])

    final_chat = get_chat_by_id(chat_doc['_id'])
    return jsonify({
        "chat": final_chat,
        "reply": dummy_reply,
    }), 200


