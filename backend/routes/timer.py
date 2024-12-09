from flask import Blueprint, jsonify
timer_bp = Blueprint('timer', __name__)

@timer_bp.route('/api/timer/<string:discord_id>', methods=['GET'])
def get_timer(discord_id):
    # For now, return a placeholder or simple JSON structure
    # Later, this can query a database or a global in-memory store for actual timing info
    return jsonify({
        'discord_id': discord_id,
        'next_prompt_in_seconds': 3600  # Example placeholder value
    }), 200

