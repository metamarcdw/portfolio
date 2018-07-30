import random

from flask import Blueprint, render_template, flash
from server.content import projects, contact_info, rights

portfolio = Blueprint("portfolio", __name__, template_folder="templates")


@portfolio.route("/")
def home():
    flash("<!-- TODO: Welcome guest. -->")
    return render_template("home.html",
                           title="Welcome",
                           right=random.choice(rights))

@portfolio.route("/portfolio")
def _portfolio():
    flash("Thanks for visiting. Please make yourself comfortable :P")
    return render_template("portfolio.html",
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
    return render_template("contact.html",
                           title="Contact Me",
                           contact=contact_info,
                           right=random.choice(rights))
