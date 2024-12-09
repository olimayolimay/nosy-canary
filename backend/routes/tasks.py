from flask import Blueprint, request, jsonify
from models import db, User, Task

bp = Blueprint('tasks', __name__, url_prefix='/api')

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    discord_id = data.get('discord_id')
    description = data.get('description')
    status = data.get('status', 'pending')
    notes = data.get('notes', '')

    user = User.query.filter_by(discord_id=discord_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = Task(user_id=user.id, description=description, status=status, notes=notes)
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created", "task_id": task.id}), 201

# GET /api/tasks/<discord_id>
# Return all tasks for the given user.
@bp.route('/tasks/<discord_id>', methods=['GET'])
def get_tasks(discord_id):
    user = User.query.filter_by(discord_id=discord_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    tasks = Task.query.filter_by(user_id=user.id).all()
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            "id": task.id,
            "description": task.description,
            "status": task.status,
            "notes": task.notes
        })
    
    return jsonify({"tasks": tasks_list}), 200

# PUT /api/tasks/<id>
# Update a task by ID. Expect JSON with fields you want to update (e.g., description, status, notes).
@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Update only provided fields
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
    if 'notes' in data:
        task.notes = data['notes']

    db.session.commit()
    return jsonify({"message": "Task updated successfully"}), 200

# DELETE /api/tasks/<id>
# Delete a task by ID.
@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"}), 200

