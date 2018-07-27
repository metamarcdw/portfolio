from flask import Flask

app = Flask(__name__)
app.secret_key = "asecret"

def create_app():
    return app

from server import routes
