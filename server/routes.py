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

#################################################################
# ----------------------- MAIN BLUEPRINT ------------------------
#################################################################
main = Blueprint("main", __name__, template_folder="templates")


@main.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        return _handle_login()
    user = "MarcDW" if current_user.is_authenticated else "Guest"
    flash(f"<!-- TODO: Welcome {user}. Thanks for visiting. -->")
    return render_template("home.html",
                           title="Welcome",
                           right=random.choice(rights))


@main.route("/portfolio", methods=["GET", "POST"])
def _portfolio():
    from server.models import Project
    if request.method == "POST":
        return _handle_login()
    projects = Project.query.all()
    projects.sort(key=lambda p: p.index)
    paths = {
        "detail": "projects",
        "edit": "edit",
        "delete": "delete",
        "moveup": "moveup"
    }
    return render_template("items.html",
                           title="Portfolio",
                           heading="MARCDW'S PORTFOLIO",
                           items=projects,
                           paths=paths,
                           right=random.choice(rights))


@main.route("/blog", methods=["GET", "POST"])
def _blog():
    from server.models import Blogpost
    if request.method == "POST":
        return _handle_login()
    blogposts = Blogpost.query.all()
    blogposts.sort(key=lambda p: p.index)
    paths = {
        "detail": "blogposts",
        "edit": "edit_post",
        "delete": "delete_post",
        "moveup": "moveup_post"
    }
    return render_template("items.html",
                           title="Blog",
                           heading="MARCDW'S BLOG",
                           items=blogposts,
                           paths=paths,
                           right=random.choice(rights))


@main.route("/contact", methods=["GET", "POST"])
def contact_view():
    if request.method == "POST":
        return _handle_login()
    return render_template("contact.html",
                           title="Contact Me",
                           contact=contact_info,
                           right=random.choice(rights))


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("main.home"))


def _is_safe_url(target):
    # http://flask.pocoo.org/snippets/62/
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and \
        ref_url.netloc == test_url.netloc


def _handle_login():
    next = None
    username_input = request.form["username_input"]
    password_input = request.form["password_input"]

    superuser = User.query.filter_by(username=username_input).first()
    if superuser and check_password_hash(superuser.password_hash, password_input):
        login_user(superuser)

        # _is_safe_url should check if the url is safe for redirects.
        next = request.form.get("next")
        if not _is_safe_url(next):
            return abort(400)
        msg = "Login Successful."
    else:
        msg = "Login Failed."
    flash(msg)
    return redirect(next or url_for("main.home"))


#################################################################
# ----------------------- PORTFOLIO BLUEPRINT -------------------
#################################################################
portfolio = Blueprint("portfolio", __name__, template_folder="templates")


@portfolio.route("/projects/<string:title>", methods=["GET", "POST"])
def projects_view(title):
    from server.models import Project
    if request.method == "POST":
        return _handle_login()
    project = Project.query.filter_by(title=title).first()
    if not project:
        abort(404)
    return render_template("project.html",
                           title=project.title,
                           project=project,
                           right=random.choice(rights))


#pylint: disable=E1101
@portfolio.route("/new", methods=["GET", "POST"])
@login_required
def new_project():
    from server import db
    from server.models import Project
    from server.forms import ProjectForm

    project_form = ProjectForm()
    if request.method == "POST":
        if project_form.validate() and "photo" in request.files:
            filename = photos.save(request.files["photo"])
            index = (db.session.query(db.func.max(Project.index)).scalar() or 0) + 1

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
            return redirect(url_for("main._portfolio"))
        else:
            flash("Project creation failed.")

    return render_template("edit_form.html",
                           form=project_form,
                           title="Create Projects",
                           right=random.choice(rights),
                           new=True)


@portfolio.route("/edit/<string:title>", methods=["GET", "POST"])
@login_required
def edit_project(title):
    from server import db
    from server.models import Project
    from server.forms import ProjectForm

    project = Project.query.filter_by(title=title).first()
    if not project:
        abort(404)
    project_form = ProjectForm(obj=project)

    if request.method == "POST":
        if project_form.validate():
            project_form.populate_obj(project)
            db.session.commit()
            flash("Edit was successful.")
            return redirect(url_for("main._portfolio"))
        else:
            flash("Project editing failed.")

    return render_template("edit_form.html",
                           form=project_form,
                           title="Edit Projects",
                           right=random.choice(rights))


@portfolio.route("/delete/<string:title>")
@login_required
def delete_project(title):
    from server import db
    from server.models import Project

    project = Project.query.filter_by(title=title).first()
    if not project:
        abort(404)
    image_path = os.path.join(os.path.dirname(__file__),
                              "static", "images", project.imgfile)
    if os.path.exists(image_path):
        os.unlink(image_path)
    db.session.delete(project)
    db.session.commit()

    flash("Delete was successful.")
    return redirect(url_for("main._portfolio"))


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

    return redirect(url_for("main._portfolio"))


#################################################################
# ----------------------- BLOG BLUEPRINT ------------------------
#################################################################
blog = Blueprint("blog", __name__, template_folder="templates")


@blog.route("/blogposts/<string:title>", methods=["GET", "POST"])
def blogpost_view(title):
    from server.models import Blogpost
    if request.method == "POST":
        return _handle_login()
    blogpost = Blogpost.query.filter_by(title=title).first()
    if not blogpost:
        abort(404)
    return render_template("blogpost.html",
                           title=blogpost.title,
                           blogpost=blogpost,
                           right=random.choice(rights))


@blog.route("/new_post", methods=["GET", "POST"])
@login_required
def new_blogpost():
    from server import db
    from server.models import Blogpost
    from server.forms import BlogpostForm

    blogpost_form = BlogpostForm()
    if request.method == "POST":
        if blogpost_form.validate() and "photo" in request.files:
            filename = photos.save(request.files["photo"])
            index = (db.session.query(db.func.max(Blogpost.index)).scalar() or 0) + 1

            blogpost = Blogpost(title=request.form["title"],
                                imgfile=filename,
                                markdown=request.form["markdown"],
                                index=index)

            db.session.add(blogpost)
            db.session.commit()
            flash("Blogpost was created.")
            return redirect(url_for("main._blog"))
        else:
            flash("Blogpost creation failed.")

    return render_template("edit_form.html",
                           form=blogpost_form,
                           title="Create Blogposts",
                           right=random.choice(rights),
                           new=True)


@blog.route("/edit_post/<string:title>", methods=["GET", "POST"])
@login_required
def edit_blogpost(title):
    from server import db
    from server.models import Blogpost
    from server.forms import BlogpostForm

    blogpost = Blogpost.query.filter_by(title=title).first()
    if not blogpost:
        abort(404)
    blogpost_form = BlogpostForm(obj=blogpost)

    if request.method == "POST":
        if blogpost_form.validate():
            blogpost_form.populate_obj(blogpost)
            db.session.commit()
            flash("Edit was successful.")
            return redirect(url_for("main._blog"))
        else:
            flash("Blogpost editing failed.")

    return render_template("edit_form.html",
                           form=blogpost_form,
                           title="Edit Blogposts",
                           right=random.choice(rights))


@blog.route("/delete_post/<string:title>", methods=["GET", "POST"])
@login_required
def delete_blogpost(title):
    from server import db
    from server.models import Blogpost

    blogpost = Blogpost.query.filter_by(title=title).first()
    if not blogpost:
        abort(404)
    image_path = os.path.join(os.path.dirname(__file__),
                              "static", "images", blogpost.imgfile)
    if os.path.exists(image_path):
        os.unlink(image_path)
    db.session.delete(blogpost)
    db.session.commit()

    flash("Delete was successful.")
    return redirect(url_for("main._blog"))


@blog.route("/moveup_post/<int:index>", methods=["GET", "POST"])
@login_required
def moveup_blogpost(index):
    from server import db
    from server.models import Blogpost

    this_blogpost = Blogpost.query.filter_by(index=index).first()
    next_blogpost = Blogpost.query.filter(
        Blogpost.index < this_blogpost.index).order_by(
            Blogpost.index.desc()).first()

    if not this_blogpost:
        abort(404)
    if next_blogpost:
        temp = this_blogpost.index
        this_blogpost.index = next_blogpost.index
        next_blogpost.index = temp
        db.session.commit()
        flash("Move was successful.")

    return redirect(url_for("main._blog"))
