from flask import Blueprint, request, jsonify
from models import db, User

user_bp = Blueprint('user_bp', __name__, url_prefix='/api/user')

@user_bp.route('/<discord_id>', methods=['GET'])
def get_user(discord_id):
    user = User.query.filter_by(discord_id=discord_id).first()
    if user:
        return jsonify({
            'id': user.id,
            'discord_id': user.discord_id,
            'canary_bedtime': user.canary_bedtime
        }), 200
    return jsonify({'error': 'User not found'}), 404

@user_bp.route('', methods=['POST'])
def create_or_update_user():
    data = request.get_json()
    discord_id = data.get('discord_id')
    canary_bedtime = data.get('canary_bedtime')

    if not discord_id:
        return jsonify({'error': 'discord_id is required'}), 400

    user = User.query.filter_by(discord_id=discord_id).first()
    if user is None:
        user = User(discord_id=discord_id, canary_bedtime=canary_bedtime)
        db.session.add(user)
    else:
        user.canary_bedtime = canary_bedtime

    db.session.commit()

    return jsonify({
        'id': user.id,
        'discord_id': user.discord_id,
        'canary_bedtime': user.canary_bedtime
    }), 200

