import pytest
from app import create_app, db
from app.models import Project, Task
from app.config import Config
from datetime import datetime, timedelta


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def init_database(app):
    with app.app_context():
        project1 = Project(name='Test Project 1', description='Description for Project 1')
        project2 = Project(name='Test Project 2', description='Description for Project 2')
        db.session.add_all([project1, project2])
        db.session.commit()

        task1 = Task(
            title='Test Task 1',
            description='Test Description 1',
            status='todo',
            priority=5,
            due_date=datetime.utcnow() + timedelta(days=1),
            project_id=project1.id
        )

        task2 = Task(
            title='Test Task 2',
            description='Test Description 2',
            status='in_progress',
            priority=2,
            project_id=project2.id
        )

        db.session.add_all([task1, task2])
        db.session.commit()

        yield {'projects': [project1, project2], 'tasks': [task1, task2]}

        db.session.remove()
        db.drop_all()
        db.create_all()
