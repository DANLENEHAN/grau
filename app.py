"""
API entry point. All routes are registered here.
"""


import uuid

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy_session import flask_scoped_session
from flask_login import LoginManager, login_required
from sqlalchemy.orm import sessionmaker

from grau.blueprints.user.routes import user_api
from grau.db.functions import get_session_maker
from grau.db.model import User
from grau.utils import get_secret_key, decrypt_str


def create_app(session_factory: sessionmaker = get_session_maker()):
    app = Flask(__name__)
    app.register_blueprint(user_api)
    add_app_config(app)

    db_session = flask_scoped_session(session_factory, app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    CORS(app)

    @login_manager.user_loader
    def load_user(user_id: str):
        """Loads a user from the database. The user ID is encrypted to
        prevent leaking the ID to the client."""
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
    def after_request(response):
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

    @app.route("/test_auth")
    @login_required
    def test_auth():
        return jsonify({"status": "user authenticated"})

    return app


def add_app_config(app: Flask):
    """
    Adds configuration to the app.
    """
    app.config["SECRET_KEY"] = get_secret_key()
    app.config["REMEMBER_COOKIE_DURATION"] = 60 * 60 * 24  # 1 day
