from flask import Blueprint, request, jsonify

from app.models import Project
from app.services.task_service import get_all_tasks, get_task_by_id, create_task, update_task, delete_task

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    priority = request.args.get('priority')
    project_id = request.args.get('project_id', type=int)

    tasks = get_all_tasks(status=status, priority=priority, project_id=project_id)
    return jsonify([task.to_dict() for task in tasks])


@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict())


@tasks_bp.route('', methods=['POST'])
def add_task():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('project_id'):
        return jsonify({'error': 'Title and project_id are required'}), 400

    project = Project.query.get(data['project_id'])
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    task = create_task(data)
    return jsonify(task.to_dict()), 201


@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def modify_task(task_id):
    data = request.get_json()
    task = get_task_by_id(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    updated_task = update_task(task, data)
    return jsonify(updated_task.to_dict())


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    task = get_task_by_id(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    delete_task(task)
    return jsonify({'message': 'Task deleted successfully'}), 200
