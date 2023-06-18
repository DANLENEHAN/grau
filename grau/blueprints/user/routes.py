from flask import Blueprint, request, session
from flask_login import login_required
from flask_sqlalchemy_session import current_session

from grau.blueprints.user import functions
from grau.blueprints.user.functions import attempt_login, attempt_logout

user_api = Blueprint("user_api", __name__)


@user_api.route("/create_user", methods=["POST"])
def create_user():
    """
    Create user endpoint for users.
    """
    return functions.create_user(current_session, request.json)


@user_api.route("/login", methods=["POST"])
def login():
    """
    Login endpoint for users.
    """
    return attempt_login(
        current_session, request.json["email"], request.json["password"]
    )


@user_api.route("/logout", methods=["POST"])
def logout():
    """
    Logout endpoint for users.
    """
    return attempt_logout(current_session, session.get("_user_id"))


@user_api.route("/reset_password")
def reset_password():
    """
    Reset password endpoint for users.
    """
    return "Reset Password"


@user_api.route("/user_authenticated", methods=["GET"])
@login_required
def test_auth():
    """
    Test authentication endpoint for users.
    """
    return "User Authenticated", 200
