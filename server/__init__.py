from flask import Flask
from server.routes import portfolio

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = "asecret"

    app.register_blueprint(portfolio)
    return app
