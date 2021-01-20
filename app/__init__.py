from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(testing):
    app = Flask(__name__, instance_relative_config=False, template_folder="templates")
    if not testing:
        app.config.from_object("config.Config")
    else:
        app.config.from_object("config.TestConfig")

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from .views import user_management, spotify_auth
        from .models import user_model

        db.drop_all()
        db.create_all()

        return app