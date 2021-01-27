from flask import Flask


def create_app(testing):
    app = Flask(__name__, instance_relative_config=False, template_folder="templates")
    if not testing:
        app.config.from_object("config.Config")
    else:
        app.config.from_object("config.TestConfig")

    with app.app_context():
        from .views import library, spotify, nav

        return app