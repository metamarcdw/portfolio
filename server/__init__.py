import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_images import Images
from flask_uploads import UploadSet, configure_uploads, IMAGES

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
    mode = os.environ.get("PORTFOLIO_MODE")
    config_type = None

    if mode == "production":
        config_type = "server.config.ProductionConfig"
    elif mode == "development":
        config_type = "server.config.DevelopmentConfig"
    else:
        raise ValueError("Mode variable not set.")
    print(f" * Running the API in {mode} mode.")

    app = Flask(__name__)
    app.config.from_object(config_type)

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
