from datetime import datetime
from typing import Any, Dict, Tuple

from sqlalchemy import and_
from sqlalchemy.orm import scoped_session

from grau.db.user_stats.user_stats_model import UserStats


def get_user_stats(db_session: scoped_session, user_id: int) -> UserStats:
    """
    Get user stats from the database.
    Args:
        db_session (scoped_session): SQLAlchemy scoped session
        user_id (int): id of the user to get stats for
    Returns:
        UserStats: UserStats object from the database
    """
    return (
        db_session.query(UserStats).filter(UserStats.user_id == user_id).all()
    )


def create_user_stats(
    db_session: scoped_session, user_stats_dict: Dict[str, Any]
) -> Tuple[str, int]:
    """
    Create user stats in the database.
    Args:
        db_session (scoped_session): SQLAlchemy scoped session
        user_stats_dict (dict[str:str]): dictionary containing user
            stats information
    Returns:
        tuple[str, int]: tuple containing the response message and status code
    """
    user_stats_dict["created_at"] = datetime.now()
    user_stats_dict["updated_at"] = datetime.now()

    user_stats = UserStats(**user_stats_dict)
    db_session.add(user_stats)
    db_session.commit()
    return "User stats created successfully", 201


def get_user_stat(
    db_session: scoped_session, user_id: int, stat_id: int
) -> UserStats:
    """
    Get individual user stat from the database.
    Args:
        db_session (scoped_session): SQLAlchemy scoped session
        user_id (int): id of the user to get stats for
        stat_id (int): id of the stat to get
    Returns:
        UserStats: UserStats object from the database
    """
    return (
        db_session.query(UserStats)
        .filter(and_(UserStats.user_id == user_id, UserStats.id == stat_id))
        .one_or_none()
    )


def update_user_stat(
    db_session: scoped_session, user_stats_dict: Dict[str, Any]
) -> Tuple[str, int]:
    """
    Update individual user stat in the database.
    """
    user_stats = get_user_stat(
        db_session, user_stats_dict["user_id"], user_stats_dict["id"]
    )
    if not user_stats:
        return "User stat not found", 404

    user_stats_dict["updated_at"] = datetime.now()

    for key, value in user_stats_dict.items():
        setattr(user_stats, key, value)
    db_session.commit()
    return "User stat updated successfully", 200


def delete_user_stat(
    db_session: scoped_session, user_id: int, stat_id: int
) -> Tuple[str, int]:
    """
    Delete individual user stat from the database.
    Args:
        db_session (scoped_session): SQLAlchemy scoped session
        user_id (int): id of the user to get stats for
        stat_id (int): id of the stat to delete
    Returns:
        tuple[str, int]: tuple containing the response message and status code
    """
    user_stats = get_user_stat(db_session, user_id, stat_id)
    if not user_stats:
        return "User stat not found", 404

    db_session.delete(user_stats)
    db_session.commit()
    return "User stat deleted successfully", 200
