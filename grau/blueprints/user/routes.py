from flask import Blueprint, request, session
from flask_login import login_required
from flask_sqlalchemy_session import current_session
from grau.blueprints.user.functions import attempt_login, attempt_logout
from grau.blueprints.user import functions

user_api = Blueprint("user_api", __name__)


@user_api.route("/create_user", methods=["POST"])
def create_user():
    return functions.create_user(current_session, request.json)


@user_api.route("/login", methods=["POST"])
def login():
    return attempt_login(
        current_session, request.json["email"], request.json["password"]
    )


@user_api.route("/logout", methods=["POST"])
def logout():
    return attempt_logout(current_session, session.get("_user_id"))


@user_api.route("/reset_password")
def reset_password():
    return "Reset Password"


@user_api.route("/user_authenticated", methods=["GET"])
@login_required
def test_auth():
    return "User Authenticated", 200
