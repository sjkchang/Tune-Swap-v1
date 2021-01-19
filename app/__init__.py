from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(testing):
    app = Flask(__name__, instance_relative_config=False, template_folder="templates")
    if not testing:
        app.config.from_object("config.Config")
    else:
        app.config.from_object("config.TestConfig")

    db.init_app(app)

    with app.app_context():
        from .views import sample_route
        from .models import sample_model

        return app