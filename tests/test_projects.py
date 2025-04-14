import json

from app import db
from app.models import Project, Task


def test_get_all_projects(client, init_database):
    response = client.get('/api/projects')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 2


def test_get_project_by_id(client, init_database):
    project_id = init_database['projects'][0].id
    response = client.get(f'/api/projects/{project_id}')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['name'] == 'Test Project 1'
    assert 'task_count' in data


def test_get_project_with_tasks(client, init_database):
    project_id = init_database['projects'][0].id
    response = client.get(f'/api/projects/{project_id}?include_tasks=true')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'tasks' in data
    assert len(data['tasks']) == 1
    assert data['tasks'][0]['title'] == 'Test Task 1'


def test_get_nonexistent_project(client):
    response = client.get('/api/projects/999')
    data = json.loads(response.data)

    assert response.status_code == 404
    assert 'error' in data


def test_create_project(client):
    project_data = {
        'name': 'New Project',
        'description': 'New Project Description'
    }

    response = client.post(
        '/api/projects',
        data=json.dumps(project_data),
        content_type='application/json'
    )

    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['name'] == 'New Project'
    assert data['description'] == 'New Project Description'

    with client.application.app_context():
        project = Project.query.filter_by(name='New Project').first()
        assert project is not None
        assert project.description == 'New Project Description'


def test_update_project(client, init_database):
    project_id = init_database['projects'][0].id
    update_data = {
        'name': 'Updated Project Name',
        'description': 'Updated Project Description'
    }

    response = client.put(
        f'/api/projects/{project_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['name'] == 'Updated Project Name'
    assert data['description'] == 'Updated Project Description'

    with client.application.app_context():
        project = Project.query.get(project_id)
        assert project.name == 'Updated Project Name'
        assert project.description == 'Updated Project Description'


def test_delete_project(client, init_database):
    project_id = init_database['projects'][0].id

    response = client.delete(f'/api/projects/{project_id}')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'message' in data

    with client.application.app_context():
        project = Project.query.get(project_id)
        assert project is None

        tasks = db.session.query(
            db.exists().where(Task.project_id == project_id)
        ).scalar()
        assert not tasks


def test_get_project_tasks(client, init_database):
    project_id = init_database['projects'][0].id
    response = client.get(f'/api/projects/{project_id}/tasks')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['title'] == 'Test Task 1'
