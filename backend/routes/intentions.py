from flask import Blueprint, request, jsonify
from models import db, User, Intention
from datetime import datetime

bp = Blueprint('intentions', __name__, url_prefix='/api')

# GET /api/intentions/<discord_id>
# Returns the user's latest intention by timestamp.
@bp.route('/intentions/<discord_id>', methods=['GET'])
def get_latest_intention(discord_id):
    user = User.query.filter_by(discord_id=discord_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Order intentions by timestamp (descending) to get the latest one
    latest_intention = Intention.query.filter_by(user_id=user.id).order_by(Intention.timestamp.desc()).first()

    if not latest_intention:
        # Return a message if the user has no intentions
        return jsonify({"message": "No intentions found for this user"}), 200
    
    return jsonify({
        "id": latest_intention.id,
        "text": latest_intention.text,
        "timestamp": latest_intention.timestamp.isoformat(),
        "user_id": user.id
    }), 200

# POST /api/intentions
# Create a new intention for the user.
# Expects JSON: {"discord_id": "user_discord_id", "text": "intention text"}
@bp.route('/intentions', methods=['POST'])
def create_intention():
    data = request.get_json()

    discord_id = data.get('discord_id')
    text = data.get('text')

    # Validate input
    if not discord_id or not text:
        return jsonify({"error": "discord_id and text are required"}), 400

    # Find the user by discord_id
    user = User.query.filter_by(discord_id=discord_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Create a new intention
    intention = Intention(user_id=user.id, text=text, timestamp=datetime.utcnow())
    db.session.add(intention)
    db.session.commit()

    return jsonify({"message": "Intention created", "intention_id": intention.id}), 201

