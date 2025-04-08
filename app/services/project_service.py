from app import db
from app.models import Project


def get_all_projects():
    return Project.query.all()


def get_project_by_id(project_id):
    return Project.query.get(project_id)


def create_project(data):
    project = Project(
        name=data['name'],
        description=data.get('description', '')
    )

    db.session.add(project)
    db.session.commit()
    return project


def update_project(project, data):
    if 'name' in data:
        project.name = data['name']
    if 'description' in data:
        project.description = data['description']

    db.session.commit()
    return project


def delete_project(project):
    db.session.delete(project)
    db.session.commit()
    return True
