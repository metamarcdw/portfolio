from datetime import datetime
from sqlalchemy_utils import URLType
from wtforms.validators import Regexp
from flask_login import UserMixin
from server import db


#pylint: disable=E1101
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, autoincrement=True)
    title = db.Column(db.String(30),
                      unique=True,
                      nullable=False,
                      info={"validators": Regexp("^[A-Za-z0-9_-]*$")})
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


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),
                      unique=True,
                      nullable=False,
                      info={"validators": Regexp("[A-Za-z0-9-_]*$")})
    imgfile = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    markdown = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Blogpost title: {self.title}>"
