from flask import Blueprint, request, jsonify
from app.services.project_service import get_all_projects, get_project_by_id, create_project, update_project, \
    delete_project

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('', methods=['GET'])
def get_projects():
    projects = get_all_projects()
    return jsonify([project.to_dict() for project in projects])


@projects_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = get_project_by_id(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    include_tasks = request.args.get('include_tasks', 'false').lower() == 'true'
    if include_tasks:
        return jsonify(project.to_dict_with_tasks())
    else:
        return jsonify(project.to_dict())


@projects_bp.route('', methods=['POST'])
def add_project():
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'error': 'Project name is required'}), 400

    project = create_project(data)
    return jsonify(project.to_dict()), 201


@projects_bp.route('/<int:project_id>', methods=['PUT'])
def modify_project(project_id):
    data = request.get_json()
    project = get_project_by_id(project_id)

    if not project:
        return jsonify({'error': 'Project not found'}), 404

    updated_project = update_project(project, data)
    return jsonify(updated_project.to_dict())


@projects_bp.route('/<int:project_id>', methods=['DELETE'])
def remove_project(project_id):
    project = get_project_by_id(project_id)

    if not project:
        return jsonify({'error': 'Project not found'}), 404

    delete_project(project)
    return jsonify({'message': 'Project deleted successfully'}), 200


@projects_bp.route('/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    project = get_project_by_id(project_id)

    if not project:
        return jsonify({'error': 'Project not found'}), 404

    return jsonify([task.to_dict() for task in project.tasks])
