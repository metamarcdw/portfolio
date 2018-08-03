import random
from flask import Blueprint, render_template, flash, request, redirect, url_for, abort

portfolio = Blueprint("portfolio", __name__, template_folder="templates")
logged_in = False

login_info = {
    "username": "admin",
    "password": "password"
}

contact_info = {
    "email": "marcdw87@gmail.com",
    "angellist": "https://angel.co/metamarcdw",
    "linkedin": "https://www.linkedin.com/in/marc-wood-6a5959122",
    "github": "https://github.com/metamarcdw",
    "twitter": "https://twitter.com/metamarcdw"
}

rights = [
    "Dwights",
    "sprites",
    "kites",
    "Lite-Brites",
    "knights"
]


@portfolio.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return handle_login()
    user = "MarcDW" if logged_in else "Guest"
    flash(f"<!-- TODO: Welcome {user}. -->")
    return render_template("home.html",
                           title="Welcome",
                           right=random.choice(rights),
                           logged_in=logged_in)


@portfolio.route("/portfolio", methods=["GET", "POST"])
def _portfolio():
    from server.models import Project
    if request.method == "POST":
        return handle_login()
    projects = Project.query.all()
    flash("Thanks for visiting. Please make yourself comfortable :P")
    return render_template("portfolio.html",
                           title="Portfolio",
                           projects=projects,
                           right=random.choice(rights),
                           logged_in=logged_in)


@portfolio.route("/projects/<int:id>", methods=["GET", "POST"])
def projects_view(id):
    from server.models import Project
    if request.method == "POST":
        return handle_login()
    project = Project.query.filter_by(id=id).first()
    if not project:
        abort(404)
    return render_template("project.html",
                           title=project.title,
                           project=project,
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


#pylint: disable=E1101
@portfolio.route("/new", methods=["GET", "POST"])
def new_project():
    from server import db
    from server.models import Project
    from server.forms import ProjectForm

    if not logged_in:
        abort(403)

    project_form = ProjectForm()
    if request.method == "POST" and project_form.validate():
        project = Project(title=request.form["title"],
                          imgfile=request.form["imgfile"],
                          website=request.form["website"],
                          github_url=request.form["github_url"],
                          abandoned=request.form.get(
                              "abandoned") is not None,
                          description=request.form["description"],
                          long_desc=request.form["long_desc"])
        db.session.add(project)
        db.session.commit()
        flash("Project was created.")
        return redirect(url_for("portfolio._portfolio"))

    return render_template("edit_project.html",
                           form=project_form,
                           title="Create Projects",
                           right=random.choice(rights),
                           logged_in=logged_in)


@portfolio.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_project(id):
    from server import db
    from server.models import Project
    from server.forms import ProjectForm

    if not logged_in:
        abort(403)

    project = Project.query.filter_by(id=id).first()
    if not project:
        abort(404)
    project_form = ProjectForm(obj=project)

    if request.method == "POST" and project_form.validate():
        project_form.populate_obj(project)
        db.session.commit()
        flash("Edit was successful.")
        return redirect(url_for("portfolio._portfolio"))

    return render_template("edit_project.html",
                           form=project_form,
                           title="Edit Projects",
                           right=random.choice(rights),
                           logged_in=logged_in)


@portfolio.route("/delete/<int:id>")
def delete_project(id):
    from server import db
    from server.models import Project

    if not logged_in:
        abort(403)

    project = Project.query.filter_by(id=id).first()
    if not project:
        abort(404)
    db.session.delete(project)
    db.session.commit()

    flash("Delete was successful.")
    return redirect(url_for("portfolio._portfolio"))


@portfolio.route("/logout")
def logout():
    global logged_in
    logged_in = False
    flash("Logged out.")
    return redirect(url_for("portfolio.home"))


def handle_login():
    global logged_in
    if request.form["username_input"] == login_info["username"] and \
            request.form["password_input"] == login_info["password"]:
        logged_in = True
        msg = "Login Successful."
    else:
        msg = "Login Failed."
    flash(msg)
    return redirect(url_for("portfolio.home"))


@portfolio.errorhandler(404)
def handle_404(e):
    return render_template("error.html",
                           error=e,
                           status=404), 404


@portfolio.errorhandler(403)
def handle_403(e):
    return render_template("error.html",
                           error=e,
                           status=403), 403


@portfolio.errorhandler(500)
def handle_500(e):
    return render_template("error.html",
                           error=e,
                           status=500), 500
