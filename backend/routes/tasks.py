import re
from flask import Blueprint, request, jsonify, current_app
from models import db, User, Task
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('tasks', __name__, url_prefix='/api')

# POST /api/tasks - Create a new task
@bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        discord_id = data.get('discord_id')
        description = data.get('description')
        status = data.get('status', 'pending')
        notes = data.get('notes', '')

        # Validate required fields
        if not discord_id or not description:
            return jsonify({"error": "discord_id and description are required"}), 400

        # Validate discord_id format
        if not re.fullmatch(r'\d{17,19}', discord_id):
            return jsonify({"error": "Invalid discord_id format"}), 400

        # Validate status
        allowed_statuses = ['pending', 'in-progress', 'completed']
        if status not in allowed_statuses:
            return jsonify({"error": f"Invalid status. Allowed statuses are {allowed_statuses}"}), 400

        user = User.query.filter_by(discord_id=discord_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        task = Task(user_id=user.id, description=description, status=status, notes=notes)
        db.session.add(task)
        db.session.commit()

        return jsonify({"message": "Task created", "task_id": task.id}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in create_task: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in create_task: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

# GET /api/tasks/<discord_id> - Retrieve all tasks for a user
@bp.route('/tasks/<discord_id>', methods=['GET'])
def get_tasks(discord_id):
    try:
        # Validate discord_id format
        if not re.fullmatch(r'\d{17,19}', discord_id):
            return jsonify({"error": "Invalid discord_id format"}), 400

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

    except SQLAlchemyError as e:
        current_app.logger.error(f"Database error in get_tasks: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in get_tasks: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

# PUT /api/tasks/<task_id> - Update a specific task
@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided for update"}), 400

        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        # Define allowed fields and their validators
        allowed_fields = {
            'description': lambda x: isinstance(x, str) and len(x.strip()) > 0,
            'status': lambda x: x in ['pending', 'in-progress', 'completed'],
            'notes': lambda x: isinstance(x, str)
        }

        updated = False  # Flag to check if any field is updated

        for field, validator in allowed_fields.items():
            if field in data:
                if not validator(data[field]):
                    return jsonify({"error": f"Invalid value for '{field}'"}), 400
                setattr(task, field, data[field])
                updated = True

        if not updated:
            return jsonify({"error": "No valid fields provided for update"}), 400

        db.session.commit()
        return jsonify({"message": "Task updated successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in update_task: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in update_task: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

# DELETE /api/tasks/<task_id> - Delete a specific task
@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task deleted successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error in delete_task: {e}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error in delete_task: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

