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

    @property
    def task_count(self):
        return self.tasks.count()

    @property
    def completed_task_count(self):
        return self.tasks.filter_by(status='done').count()

    @property
    def progress_percentage(self):
        if self.task_count == 0:
            return 0
        return int((self.completed_task_count / self.task_count) * 100)


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
