from flask import Blueprint, request, session
from flask_login import login_required
from flask_sqlalchemy_session import current_session

from grau.blueprints.user_stats import functions

user_stats_api = Blueprint("user_stats_api", __name__)


@user_stats_api.route("/create_user_stat", methods=["POST"])
@login_required
def create_user_stat():
    """
    Create user_stat endpoint for user_stats.

    Expects:
        user_stats_dict: dict of user_stats data to create
    """
    stats_content = request.json["user_stat_dict"]

    return functions.create_user_stats(
        db_session=current_session, user_stats_dict=stats_content
    )


@user_stats_api.route("/get_user_stats", methods=["GET"])
@login_required
def get_user_stats():
    """
    Get user_stats endpoint for user_stats.
    """
    user_id = request.json["user_id"]

    return functions.get_user_stats(
        db_session=current_session, user_id=user_id
    )


@user_stats_api.route("/get_user_stat", methods=["GET"])
@login_required
def get_user_stat():
    """
    Get user_stats endpoint for user_stats.
    """
    stats_content = request.json["user_stats_dict"]
    return functions.get_user_stat(
        db_session=current_session,
        user_id=stats_content["user_id"],
        stat_id=stats_content["id"],
    )


@user_stats_api.route("/update_user_stat", methods=["PUT"])
@login_required
def update_user_stat():
    """
    Update user_stats endpoint for user_stats.

    Expects:
        user_stats_dict: dict of user_stats data to update
    """

    stats_content = request.json["user_stats_dict"]
    return functions.update_user_stat(
        db_session=current_session, user_stats_dict=stats_content
    )


@user_stats_api.route("/delete_user_stat", methods=["DELETE"])
@login_required
def delete_user_stat():
    """
    Delete user_stats endpoint for user_stats.

    Expects:
        user_stats_dict: dict of user_stats data to delete
    """

    stats_content = request.json["user_stats_dict"]
    return functions.delete_user_stat(
        db_session=current_session,
        user_id=stats_content["user_id"],
        stat_id=stats_content["id"],
    )
