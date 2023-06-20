from flask import Blueprint, request, session
from flask_login import login_required
from flask_sqlalchemy_session import current_session

from grau.blueprints.user_stats import functions

user_stats_api = Blueprint("user_stats_api", __name__)


@user_stats_api.route("/create_user_stats", methods=["POST"])
@login_required
def create_user_stats():
    """
    Create user_stats endpoint for user_stats.

    Expects:
        user_stats_dict: dict of user_stats data to create
    """
    stats_content = request.json["user_stats_dict"]
    stats_content["user_id"] = session.get("_user_id")

    return functions.create_user_stats(
        db_session=current_session, user_stats_dict=stats_content
    )


@user_stats_api.route("/get_user_stats", methods=["GET"])
@login_required
def get_user_stats():
    """
    Get user_stats endpoint for user_stats.
    """
    return functions.get_user_stats(
        db_session=current_session, user_id=session.get("_user_id")
    )


@user_stats_api.route("/update_user_stats", methods=["PUT"])
@login_required
def update_user_stats():
    """
    Update user_stats endpoint for user_stats.

    Expects:
        user_stats_dict: dict of user_stats data to update
    """

    stats_content = request.json["user_stats_dict"]
    stats_content["user_id"] = session.get("_user_id")

    return functions.update_user_stats(
        db_session=current_session, user_stats_dict=stats_content
    )


@user_stats_api.route("/delete_user_stats", methods=["DELETE"])
@login_required
def delete_user_stats():
    """
    Delete user_stats endpoint for user_stats.

    Expects:
        user_stats_dict: dict of user_stats data to delete
    """

    stats_content = request.json["user_stats_dict"]
    stats_content["user_id"] = session.get("_user_id")

    return functions.delete_user_stats(
        db_session=current_session, user_stats_dict=stats_content
    )
