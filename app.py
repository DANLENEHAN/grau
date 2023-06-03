"""
API entry point. All routes are registered here.
"""


import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.orm import sessionmaker

from grau.db.functions import get_session_maker
from grau.blueprints.user.routes import user_api


def create_app(session_factory: sessionmaker = get_session_maker()):
    app = Flask(__name__)
    app.register_blueprint(user_api)
    # Set up database session, needed to use current_session
    session = flask_scoped_session(session_factory, app)
    CORS(app)

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

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/test_db")
    def test_db():
        session.bind.engine.connect()
        return "ok"

    return app
