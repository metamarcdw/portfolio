from flask import render_template, flash
from server import app

@app.route("/")
def index():
    flash("This is a flash message.")  # TODO: Remove example flash
    return render_template("index.html", title="Portfolio")
