import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


secret_path = os.path.join(os.path.dirname(__file__), "secrets.json")
try:
    with open(secret_path, "r") as file_:
        secrets = json.load(file_)
except FileNotFoundError as e:
    raise FileNotFoundError(
        "\n * Secret file:" +
        f"\n\t{secret_path}\n   does not exist.") from e

keys = ("username", "password_hash", "secret")
if not secrets or not all([key in secrets for key in keys]):
    raise ValueError(
        "\n * Secret file:" +
        f"\n\t{secret_path}\n   is not complete.")

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)

    app.debug = True
    app.secret_key = "asecret"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        r"sqlite:///C:\Users\cypher\Desktop\portfolio\server\db.sqlite3"

    db.init_app(app)
    csrf.init_app(app)

    #pylint: disable=W0612
    @app.shell_context_processor
    def make_shell_context():
        from server.models import Project
        return {
            "db": db,
            "Project": Project
        }

    from server.routes import portfolio
    app.register_blueprint(portfolio)
    return app
