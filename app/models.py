from app.database import db
from datetime import datetime, timezone
from sqlalchemy import Enum


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#3498db')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    tasks = db.relationship('Task', backref='project', lazy='dynamic', cascade='all, delete-orphan')


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(Enum('todo', 'in_progress', 'done', name='task_status'),
                       default='todo')  # todo, in_progress, done
    priority = db.Column(db.Integer, default=1)  # 1 (low) to 5 (high)
    due_date = db.Column(db.DateTime, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))
