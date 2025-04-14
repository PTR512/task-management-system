from flask import Flask
from flask_cors import CORS
from app.database import db

from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    CORS(app)

    from app.routes.tasks import tasks_bp
    from app.routes.projects import projects_bp

    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')

    @app.route('/api/health')
    def health_check():
        return {"status": "healthy"}

    return app
