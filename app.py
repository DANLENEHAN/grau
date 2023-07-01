"""
API entry point. All routes are registered here.
"""


import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy.orm import sessionmaker

from grau.blueprints.user.routes import user_api
from grau.db.functions import get_session_maker
from grau.db.user.user_model import User
from grau.exceptions.exception_handlers import handle_grau_exception
from grau.exceptions.grau_exceptions import (BadRequest, GrauException,
                                             ResourceAlreadyExists,
                                             ResourceNotFound)
from grau.utils import decrypt_str, get_secret_key


def create_app(session_factory: sessionmaker = get_session_maker()) -> Flask:
    """
    Creates the Flask app and registers the blueprints.
    Args:
        session_factory (sessionmaker): SQLAlchemy session factory
    Returns:
        Flask: Flask app
    """
    app = Flask(__name__)
    app.register_blueprint(user_api)
    add_app_config(app)
    register_error_handlers(app)

    db_session = flask_scoped_session(session_factory, app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    CORS(app)

    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        """
        Function loads a user from the database. The user ID is encrypted to
        prevent leaking the ID to the client.
        Args:
            user_id (str): encrypted user ID
        Returns:
            User: User object from the database
        """
        print(f"Loading user with encrypted ID: {user_id}")
        return (
            db_session.query(User)
            .filter(User.session_id == decrypt_str(user_id))
            .one_or_none()
        )

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
    def after_request(response: Flask.response_class) -> Flask.response_class:
        """After request hook removes the request ID from the request
        environment. This is to ensure that the request ID is not
        leaked to the client. Could be left in for debugging purposes
        on the frontend."""

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
        db_session.bind.engine.connect()
        return "ok"

    return app


def add_app_config(app: Flask) -> None:
    """
    Adds configuration to the app.
    """
    app.config["SECRET_KEY"] = get_secret_key()
    app.config["REMEMBER_COOKIE_DURATION"] = 60 * 60 * 24  # 1 day


def register_error_handlers(app: Flask) -> None:
    """
    Registers error handlers for the app.
    """
    for exception in [
        GrauException,
        ResourceNotFound,
        ResourceAlreadyExists,
        BadRequest,
    ]:
        app.register_error_handler(exception, handle_grau_exception)
