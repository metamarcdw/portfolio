import random

from flask import Blueprint, render_template, flash
from server.content import projects, rights

portfolio = Blueprint("portfolio", __name__, template_folder="templates")


@portfolio.route("/")
def index():
    flash("Thanks for visiting. Please make yourself comfortable :P")
    return render_template("index.html",
                           title="Portfolio",
                           projects=projects,
                           right=random.choice(rights))


@portfolio.route("/projects/<int:id>")
def projects_view(id):
    return render_template("project.html",
                           title=projects[id]["title"],
                           project=projects[id],
                           right=random.choice(rights))


@portfolio.route("/contact")
def contact_view():
    return render_template("contact.html")
