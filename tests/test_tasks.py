import json

from app.models import Task


def test_get_all_tasks(client, init_database):
    response = client.get('/api/tasks')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 2


def test_get_task_by_id(client, init_database):
    task_id = init_database['tasks'][0].id
    response = client.get(f'/api/tasks/{task_id}')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['title'] == 'Test Task 1'
    assert data['status'] == 'todo'


def test_get_nonexistent_task(client):
    response = client.get('/api/tasks/999')
    data = json.loads(response.data)

    assert response.status_code == 404
    assert 'error' in data


def test_create_task(client, init_database):
    project_id = init_database['projects'][0].id
    task_data = {
        'title': 'New Task',
        'description': 'New Description',
        'status': 'todo',
        'priority': 1,
        'project_id': project_id
    }

    response = client.post(
        '/api/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )

    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['title'] == 'New Task'
    assert data['priority'] == 1

    with client.application.app_context():
        task = Task.query.filter_by(title='New Task').first()
        assert task is not None
        assert task.description == 'New Description'


def test_update_task(client, init_database):
    task_id = init_database['tasks'][0].id
    update_data = {
        'status': 'in_progress',
        'priority': 1
    }

    response = client.put(
        f'/api/tasks/{task_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )

    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['status'] == 'in_progress'
    assert data['priority'] == 1

    with client.application.app_context():
        task = Task.query.get(task_id)
        assert task.status == 'in_progress'
        assert task.priority == 1


def test_delete_task(client, init_database):
    task_id = init_database['tasks'][0].id

    response = client.delete(f'/api/tasks/{task_id}')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'message' in data

    with client.application.app_context():
        task = Task.query.get(task_id)
        assert task is None


def test_filter_tasks_by_status(client, init_database):
    response = client.get('/api/tasks?status=todo')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['status'] == 'todo'


def test_filter_tasks_by_project(client, init_database):
    project_id = init_database['projects'][0].id
    response = client.get(f'/api/tasks?project_id={project_id}')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['project_id'] == project_id
