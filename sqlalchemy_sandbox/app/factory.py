from flask import Flask


def create_test_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.default_settings")
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["TEST_APP_DATABASE_URI"]
    return app
