from flask import Blueprint, request
import app
from marshmallow import ValidationError
from grau.db.validation_schemas import UserSchema
from grau.blueprints.user import functions

user_api = Blueprint("user_api", __name__)


@user_api.route("/create_user", methods=["POST"])
def create_user():
    try:
        user = UserSchema().load(request.json)
        return functions.create_user(app.Session(), user)
    except ValidationError as exception:
        return exception.messages, 400


@user_api.route("/login")
def login():
    return "Login"


@user_api.route("/logout")
def logout():
    return "Logout"


@user_api.route("/profile")
def profile():
    return "Profile"


@user_api.route("/reset_password")
def reset_password():
    return "Reset Password"
