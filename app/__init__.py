from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accountant.db'


def create_app():
    """Add other app properties"""
    app.app_context().push()
    return app
