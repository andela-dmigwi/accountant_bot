from flask import Flask

app = Flask(__name__)


def create_app():
    """Add other app properties"""
    app.app_context().push()
    return app
