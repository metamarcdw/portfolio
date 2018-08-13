import os
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_images import Images
from flask_uploads import UploadSet, configure_uploads, IMAGES

secret_path = os.path.join(os.path.dirname(__file__), "secrets.json")
try:
    with open(secret_path, "r") as file_:
        secrets = json.load(file_)
except FileNotFoundError as e:
    raise FileNotFoundError(
        "\n * Secret file:" +
        f"\n\t{secret_path}\n   does not exist.") from e

keys = ("secret", "db_pswd")
if not secrets or not all([key in secrets for key in keys]):
    raise ValueError(
        "\n * Secret file:" +
        f"\n\t{secret_path}\n   is not complete.")

db = SQLAlchemy()
migrate = Migrate(db=db)
csrf = CSRFProtect()
login = LoginManager()
images = Images()
photos = UploadSet("photos", IMAGES)


@login.user_loader
def load_user(user_id):
    from server.models import User
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)

    app.debug = True
    app.secret_key = secrets["secret"]
    app.config["IMAGES_PATH"] = ["static/images"]
    app.config["UPLOADED_PHOTOS_DEST"] = "server/static/images"

    db_user = "marcdw87"
    db_pswd = secrets["db_pswd"]
    db_host = "localhost"
    db_name = "portfolio"
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        f"mysql://{db_user}:{db_pswd}@{db_host}/{db_user}${db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_POOL_SIZE"] = 10
    app.config["SQLALCHEMY_POOL_RECYCLE"] = 280

    db.init_app(app)
    migrate.init_app(app)
    csrf.init_app(app)
    login.init_app(app)
    images.init_app(app)
    configure_uploads(app, photos)

    #pylint: disable=W0612
    @app.shell_context_processor
    def make_shell_context():
        from server.models import Project, User
        return {
            "db": db,
            "Project": Project,
            "User": User
        }

    from server.routes import portfolio
    app.register_blueprint(portfolio)
    return app
