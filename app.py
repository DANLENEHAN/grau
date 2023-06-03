"""
API entry point. All routes are registered here.
"""


import uuid

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy_session import flask_scoped_session

from grau.db.functions import get_session_maker
from grau.blueprints.user.routes import user_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_api)
session = flask_scoped_session(get_session_maker(), app)


@app.before_request
def before_request():
    """
    Before request hook. Set request ID.
    Helps with debugging and tracing requests.
    """
    request_id = str(uuid.uuid4())
    print(f"Before Request '{request_id}'")
    request.environ["request_id"] = request_id


@app.after_request
def after_request(response):
    """
    After request hook removes the request ID from the request
    environment. This is to ensure that the request ID is not
    leaked to the client. Could be left in for debugging purposes
    on the frontend.
    """
    print(f"After request ID: '{request.environ['request_id']}'")
    request.environ.pop("request_id")
    return response


@app.route("/")
def index():
    return "You've reached the resistance."
