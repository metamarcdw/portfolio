from sqlalchemy_utils import URLType
from server import db

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
