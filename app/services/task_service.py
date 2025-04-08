from datetime import datetime
from app import db
from app.models import Task


def get_all_tasks(status=None, priority=None, project_id=None):
    query = Task.query

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if project_id:
        query = query.filter(Task.project_id == project_id)

    return query.all()


def get_task_by_id(task_id):
    return Task.query.get(task_id)


def create_task(data):
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'todo'),
        priority=data.get('priority', 'medium'),
        project_id=data['project_id']
    )

    if 'due_date' in data and data['due_date']:
        task.due_date = datetime.fromisoformat(data['due_date'])

    db.session.add(task)
    db.session.commit()
    return task


def update_task(task, data):
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
    if 'priority' in data:
        task.priority = data['priority']
    if 'due_date' in data:
        task.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
    if 'project_id' in data:
        from app.models import Project
        project = Project.query.get(data['project_id'])
        if project:
            task.project_id = data['project_id']

    db.session.commit()
    return task


def delete_task(task):
    db.session.delete(task)
    db.session.commit()
    return True