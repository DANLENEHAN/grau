from flask import Blueprint, request, session
from flask_login import login_required
from flask_sqlalchemy_session import current_session

from grau.blueprints.user import functions
from grau.db.enums import RequestType
from grau.handlers.api_response_handlers import APIResponseHandler

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
      security: []
      responses:
        '201':
          description: User created successfully
        '409':
          description: User already exists
    """

    return APIResponseHandler(
        request_type=RequestType.POST,
        response_body=functions.create_user(current_session, request.json),
    ).response


@user_api.route("/login", methods=["POST"])
def login():
    """
    post:
      tags:
          - Users
      summary: Login a user
      description: Logs in and returns the authentication cookie
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
      security: []
      responses:
        '201':
          description: >
            Login successful
            Note: The below doesn't actually work but is important
            for understanding how the login/logout and session
            management system works. See issue here:
            https://github.com/swagger-api/swagger-ui/issues/5596
            The session ID is returned in the Response headers
            `Set-Cookie` headers `session` key. You need to include
            this cookie in subsequent requests. If using Swagger UI,
            you can find the cookie in the network tab of the
            developer tools. Add the cookie to the request headers
            by clicking the Lock/Authorize button in the UI at the
            top of page for global authorization or on a per request
            basis at the endpoint level.
          headers:
            Set-Cookie:
              schema:
                type: string
                example: session=.eJwlzstOwkAUgOF3m; HttpOnly; Path=/
        '401':
          description: Login failed
    """
    return APIResponseHandler(
        request_type=RequestType.POST,
        response_body=functions.attempt_login(
            current_session, request.json["email"], request.json["password"]
        ),
    ).response


@user_api.route("/logout", methods=["POST"])
def logout():
    """
    post:
      tags:
        - Users
      summary: Logout a user.
      description: Logout a user.
      security:
        - cookieAuth: []
      responses:
        '201':
          description: Logout successful
        '400':
          description: Logout failed due to invalid credentials
    """
    return APIResponseHandler(
        request_type=RequestType.POST,
        response_body=functions.attempt_logout(
            current_session, session.get("_user_id")
        ),
    ).response


@user_api.route("/user_authenticated", methods=["GET"])
@login_required
def test_auth():
    """
    get:
      tags:
        - Users
      summary: Test authentication.
      description: Test authentication.
      security:
        - cookieAuth: []
      responses:
        '200':
          description: User authenticated
        '500':
          description: User not authenticated
    """
    return APIResponseHandler(
        request_type=RequestType.GET, response_body="User Authenticated"
    ).response
