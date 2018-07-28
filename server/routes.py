import random

from flask import render_template, flash
from server import app
from server.content import projects, rights

@app.route("/")
def index():
    flash("Thanks for visiting. Please make yourself comfortable :P")
    return render_template(
        "index.html", title="Portfolio", projects=projects, right=random.choice(rights))

@app.route("/projects/<int:id>")
def projects_view(id):
    return render_template(
        "project.html", data=projects[id], right=random.choice(rights))
