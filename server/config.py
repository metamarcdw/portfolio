import os
import json

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


class Config:
    SECRET_KEY = secrets["secret"]
    IMAGES_PATH = ["static/images"]
    UPLOADED_PHOTOS_DEST = "server/static/images"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    db_user = "marcdw87"
    db_pswd = secrets["db_pswd"]
    db_host = "marcdw87.mysql.pythonanywhere-services.com"
    db_name = "portfolio"
    SQLALCHEMY_DATABASE_URI = f"mysql://{db_user}:{db_pswd}@{db_host}/{db_user}${db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_RECYCLE = 280


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///C:\Users\cypher\Desktop\portfolio\server\db.sqlite3"
