from flask import Blueprint, request, session
from flask_login import login_required
from flask_sqlalchemy_session import current_session

from grau.blueprints.user import functions
from grau.blueprints.user.functions import attempt_login, attempt_logout

user_api = Blueprint("user_api", __name__)


@user_api.route("/create_user", methods=["POST"])
def create_user():
    """
    post:
      tags:
          - Users
      summary: Create a new user.
      description: Create a new user.
      requestBody:
        description: User object to be created
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserSchema'
      responses:
        '201':
          description: User created successfully
        '409':
          description: User already exists
    """
    return functions.create_user(current_session, request.json)


@user_api.route("/login", methods=["POST"])
def login():
    """
    post:
      tags:
          - Users
      summary: Login a user.
      description: Login a user.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                  example: dan@gmail.com
                password:
                  type: string
                  example: RLp6^$L2Ro
      responses:
        '200':
          description: Login successful
        '401':
          description: Login failed
    """
    return attempt_login(
        current_session, request.json["email"], request.json["password"]
    )


@user_api.route("/logout", methods=["POST"])
def logout():
    """
    post:
      tags:
        - Users
      summary: Logout a user.
      description: Logout a user.
      responses:
        '200':
          description: Logout successful
        '400':
          description: Logout failed due to invalid credentials
    """
    return attempt_logout(current_session, session.get("_user_id"))


@user_api.route("/user_authenticated", methods=["GET"])
@login_required
def test_auth():
    """
    get:
      tags:
        - Users
      summary: Test authentication.
      description: Test authentication.
      responses:
        '200':
          description: User authenticated
        '500':
          description: User not authenticated
    """
    return "User Authenticated", 200
