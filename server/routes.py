from flask import render_template, flash
from server import app
from server.content import projects

@app.route("/")
def index():
    flash("Thanks for visiting. Please make yourself comfortable :P")
    return render_template("index.html", title="Portfolio", projects=projects)

@app.route("/nowallet")
def nowallet():
    return render_template("project.html", data=projects[0])

@app.route("/component")
def component():
    return render_template("project.html", data=projects[1])

@app.route("/fullstack")
def fullstack():
    return render_template("project.html", data=projects[2])

@app.route("/chip8")
def chip8():
    return render_template("project.html", data=projects[3])

@app.route("/bitmessage")
def bitmessage():
    return render_template("project.html", data=projects[4])

@app.route("/metamarket")
def metamarket():
    return render_template("project.html", data=projects[5])
