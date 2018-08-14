import os
import random
from urllib.parse import urlparse, urljoin
from flask import (
    Blueprint, render_template, flash, request, redirect, url_for, abort
)
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from server.models import User
from server import photos

portfolio = Blueprint("portfolio", __name__, template_folder="templates")

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
    user = "MarcDW" if current_user.is_authenticated else "Guest"
    flash(f"<!-- TODO: Welcome {user}. Thanks for visiting. -->")
    return render_template("home.html",
                           title="Welcome",
                           right=random.choice(rights))


@portfolio.route("/portfolio", methods=["GET", "POST"])
def _portfolio():
    from server.models import Project
    if request.method == "POST":
        return handle_login()
    projects = Project.query.all()
    projects.sort(key=lambda p: p.index)
    return render_template("portfolio.html",
                           title="Portfolio",
                           projects=projects,
                           right=random.choice(rights))


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
                           right=random.choice(rights))


@portfolio.route("/contact", methods=["GET", "POST"])
def contact_view():
    if request.method == "POST":
        return handle_login()
    return render_template("contact.html",
                           title="Contact Me",
                           contact=contact_info,
                           right=random.choice(rights))


#pylint: disable=E1101
@portfolio.route("/new", methods=["GET", "POST"])
@login_required
def new_project():
    from server import db
    from server.models import Project
    from server.forms import ProjectForm

    project_form = ProjectForm()
    if request.method == "POST" and project_form.validate() and "photo" in request.files:
        filename = photos.save(request.files["photo"])
        index = db.session.query(db.func.max(Project.index)).scalar() + 1
        project = Project(title=request.form["title"],
                          imgfile=filename,
                          website=request.form["website"],
                          github_url=request.form["github_url"],
                          abandoned=request.form.get(
                              "abandoned") is not None,
                          description=request.form["description"],
                          long_desc=request.form["long_desc"],
                          index=index)
        db.session.add(project)
        db.session.commit()
        flash("Project was created.")
        return redirect(url_for("portfolio._portfolio"))
    else:
        flash("Project creation failed.")

    return render_template("edit_project.html",
                           form=project_form,
                           title="Create Projects",
                           right=random.choice(rights),
                           new=True)


@portfolio.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):
    from server import db
    from server.models import Project
    from server.forms import ProjectForm

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
                           right=random.choice(rights))


@portfolio.route("/delete/<int:id>")
@login_required
def delete_project(id):
    from server import db
    from server.models import Project

    project = Project.query.filter_by(id=id).first()
    if not project:
        abort(404)
    image_path = os.path.join(os.path.dirname(__file__),
                              "static", "images", project.imgfile)
    if os.path.exists(image_path):
        os.unlink(image_path)
    db.session.delete(project)
    db.session.commit()

    flash("Delete was successful.")
    return redirect(url_for("portfolio._portfolio"))


@portfolio.route("/moveup/<int:index>")
@login_required
def moveup_project(index):
    from server import db
    from server.models import Project

    this_project = Project.query.filter_by(index=index).first()
    next_project = Project.query.filter(
        Project.index < this_project.index).order_by(
            Project.index.desc()).first()

    if not this_project:
        abort(404)
    if next_project:
        temp = this_project.index
        this_project.index = next_project.index
        next_project.index = temp
        db.session.commit()
        flash("Move was successful.")

    return redirect(url_for("portfolio._portfolio"))


@portfolio.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("portfolio.home"))


def is_safe_url(target):
    # http://flask.pocoo.org/snippets/62/
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and \
        ref_url.netloc == test_url.netloc


def handle_login():
    next = None
    username_input = request.form["username_input"]
    password_input = request.form["password_input"]

    superuser = User.query.filter_by(username=username_input).first()
    if superuser and check_password_hash(superuser.password_hash, password_input):
        login_user(superuser)

        # is_safe_url should check if the url is safe for redirects.
        next = request.form.get("next")
        if not is_safe_url(next):
            return abort(400)
        msg = "Login Successful."
    else:
        msg = "Login Failed."
    flash(msg)
    return redirect(next or url_for("portfolio.home"))


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
                           error="Internal Server Error",
                           status=500), 500
