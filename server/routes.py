import random

from flask import Blueprint, render_template, flash, request, redirect, url_for
from server.content import projects, contact_info, rights, login_info

portfolio = Blueprint("portfolio", __name__, template_folder="templates")
logged_in = False


@portfolio.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return handle_login()
    flash("<!-- TODO: Welcome guest. -->")
    return render_template("home.html",
                           title="Welcome",
                           right=random.choice(rights),
                           logged_in=logged_in)


@portfolio.route("/portfolio", methods=["GET", "POST"])
def _portfolio():
    if request.method == "POST":
        return handle_login()
    flash("Thanks for visiting. Please make yourself comfortable :P")
    return render_template("portfolio.html",
                           title="Portfolio",
                           projects=projects,
                           right=random.choice(rights),
                           logged_in=logged_in)


@portfolio.route("/projects/<int:id>", methods=["GET", "POST"])
def projects_view(id):
    if request.method == "POST":
        return handle_login()
    return render_template("project.html",
                           title=projects[id]["title"],
                           project=projects[id],
                           right=random.choice(rights),
                           logged_in=logged_in)


@portfolio.route("/contact", methods=["GET", "POST"])
def contact_view():
    if request.method == "POST":
        return handle_login()
    return render_template("contact.html",
                           title="Contact Me",
                           contact=contact_info,
                           right=random.choice(rights),
                           logged_in=logged_in)


@portfolio.route("/fail")
def login_fail():
    return render_template("login_fail.html")


@portfolio.route("/logout")
def logout():
    global logged_in
    logged_in = False
    return redirect(url_for("portfolio.home"))


def handle_login():
    global logged_in
    if request.form["username_input"] == login_info["username"] and \
            request.form["password_input"] == login_info["password"]:
        logged_in = True
        # return redirect(url_for("portfolio.edit_projects"))
    else:
        return redirect(url_for("portfolio.login_fail"))
