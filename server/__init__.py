from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from server.routes import portfolio

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.debug = True
    app.secret_key = "asecret"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        r"sqlite:///C:\Users\cypher\Desktop\portfolio\server\db.sqlite3"

    db.init_app(app)

    #pylint: disable=W0612
    @app.shell_context_processor
    def make_shell_context():
        from server.models import Project
        return {
            "db": db,
            "Project": Project
        }

    app.register_blueprint(portfolio)
    return app
