from sqlalchemy_utils import URLType
from flask_login import UserMixin
from server import db, secrets


#pylint: disable=E1101
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    imgfile = db.Column(db.String(30), nullable=False)
    website = db.Column(URLType, nullable=True)
    github_url = db.Column(URLType, nullable=False)
    abandoned = db.Column(db.Boolean)
    description = db.Column(db.Text, nullable=False)
    long_desc = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Project title: {self.title}>"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User username: {self.username}>"
