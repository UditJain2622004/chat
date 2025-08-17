from flask import Blueprint, request, jsonify
from controllers.bot_controller import (
    create_bot,
    get_bot_by_id,
    list_bots,
    update_bot,
    delete_bot,
    get_bots_by_user_id,
)


bots_bp = Blueprint('bots', __name__)


@bots_bp.route('/', methods=['POST'])
def route_create_bot():
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400
    inserted_id = create_bot(data)
    return jsonify({"_id": inserted_id}), 201


@bots_bp.route('/', methods=['GET'])
def route_list_bots():
    user_id = request.args.get('user_id')
    if user_id:
        bots = get_bots_by_user_id(user_id)
    else:
        bots = list_bots()
    return jsonify(bots), 200


@bots_bp.route('/<bot_id>', methods=['GET'])
def route_get_bot(bot_id: str):
    bot = get_bot_by_id(bot_id)
    if not bot:
        return jsonify({"message": "Bot not found"}), 404
    return jsonify(bot), 200


@bots_bp.route('/<bot_id>', methods=['PUT', 'PATCH'])
def route_update_bot(bot_id: str):
    update_fields = request.get_json(silent=True) or {}
    modified = update_bot(bot_id, update_fields)
    if modified == 0:
        return jsonify({"message": "No changes or bot not found"}), 404
    return jsonify({"modified": modified}), 200


@bots_bp.route('/<bot_id>', methods=['DELETE'])
def route_delete_bot(bot_id: str):
    deleted = delete_bot(bot_id)
    if deleted == 0:
        return jsonify({"message": "Bot not found"}), 404
    return jsonify({"deleted": deleted}), 200


@bots_bp.route('/user/<user_id>', methods=['GET'])
def route_get_bots_by_user(user_id: str):
    bots = get_bots_by_user_id(user_id)
    return jsonify(bots), 200


