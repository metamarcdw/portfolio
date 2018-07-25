from flask import Flask

app = Flask(__name__)

def create_app():
    return app

from server import routes
