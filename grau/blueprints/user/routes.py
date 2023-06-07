from flask import Blueprint, request, session
from flask_sqlalchemy_session import current_session
from marshmallow import ValidationError

from grau.db.validation_schemas import UserSchema
from grau.blueprints.user.functions import attempt_login, attempt_logout
from grau.blueprints.user import functions

user_api = Blueprint("user_api", __name__)


@user_api.route("/create_user", methods=["POST"])
def create_user():
    try:
        user = UserSchema().load(request.json)
        return functions.create_user(current_session, user)
    except ValidationError as exception:
        return exception.messages, 400


@user_api.route("/login", methods=["POST"])
def login():
    return attempt_login(
        current_session, request.json["email"], request.json["password"]
    )


@user_api.route("/logout", methods=["POST"])
def logout():
    return attempt_logout(current_session, session.get("_user_id"))


@user_api.route("/profile")
def profile():
    return "Profile"


@user_api.route("/reset_password")
def reset_password():
    return "Reset Password"
