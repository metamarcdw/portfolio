from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

from server import db
from server.models import Project

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ["imgfile"]

    field_names = ("title", "website",
                   "github_url", "abandoned",
                   "description", "long_desc")
