"""
API entry point. All routes are registered here.
"""

import time
import uuid

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy_session import flask_scoped_session

from grau.db.functions import get_session_factory
from grau.blueprints.user.routes import user_api

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_api)
session = flask_scoped_session(get_session_factory(), app)

@app.before_request
def before_request():
    request_id = str(uuid.uuid4())
    print(f"Before Request '{request_id}'")
    request.environ["request_id"] = request_id


@app.after_request
def after_request(response):
    """
    https://docs.sqlalchemy.org/en/20/orm/contextual.html
    The Session is successfully removed because the scoped_session object
    pins a request to a single session identified by the thread the request
    is running on.
    """
    print(f"After request ID: '{request.environ['request_id']}'")
    request.environ.pop("request_id")
    return response


@app.route("/")
def index():
    return "You've reached the resistance."


@app.route("/sleep")
def sleep():
    """
    Testing the session registry. The allocation of sessions and
    session hashes. Sending requests while this endpoint sleeps
    and seeing how the session hashes change and how the session
    is created and closed.
    """
    print("Sleeping for 20 seconds")
    time.sleep(20)
    return "Slept for 20 seconds."
