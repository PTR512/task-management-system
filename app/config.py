import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/task_management'
    SQLALCHEMY_TRACK_MODIFICATIONS = False