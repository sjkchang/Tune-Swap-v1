from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=False, template_folder="templates")
    app.config.from_object("config.Config")

    with app.app_context():
        from .views import library, auth, nav

        return app