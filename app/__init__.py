from flask import Flask
from app.models import db

app = Flask(__name__)


def create_app():
    """Add other app properties"""
    app.config.from_object('config.Config')
    app.app_context().push()
    db.init_app(app)
    return app
