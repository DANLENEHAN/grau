import os
from datetime import datetime

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from grau.db.enums import DateFormat


def get_db_engine() -> Engine:
    """Get the database engine."""
    db_url = os.environ.get("DATABASE_URL")
    db_url = db_url or "postgresql+psycopg2://dan:testing123@localhost/train"
    return create_engine(db_url)


def get_session_maker() -> sessionmaker:
    """Get the session maker."""
    return sessionmaker(bind=get_db_engine())


def datetime_to_string(
    date: datetime, date_format: DateFormat = DateFormat.YMD
) -> str:
    """Convert a datetime object to a string."""
    return date.strftime(date_format.value)


def validate_date_field(
    date: str, date_format: DateFormat = DateFormat.YMD.value
):
    """Validate a date string based on date format"""
    try:
        datetime.strptime(date, date_format)
    except ValueError:
        return False
    return True
