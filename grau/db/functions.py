import os
from datetime import datetime

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from grau.db.enums import DateFormat


def get_db_engine() -> Engine:
    """
    Get the database engine.

    Returns:
        Engine: SQLAlchemy database engine
    """
    db_url = os.environ.get("DATABASE_URL")
    db_url = db_url or "postgresql+psycopg2://dan:testing123@localhost/train"
    return create_engine(db_url)


def get_session_maker() -> sessionmaker:
    """
    Get the session maker.

    Returns:
        sessionmaker: SQLAlchemy session maker
    """
    return sessionmaker(bind=get_db_engine())


def datetime_to_string(
    date: datetime, date_format: DateFormat = DateFormat.YMD
) -> str:
    """
    Convert a datetime object to a string.

    Args:
        date (datetime): datetime object to convert
        date_format (DateFormat): date format to convert to
    Returns:
        str: date string
    """
    return date.strftime(date_format.value)


def validate_date_field(date: str, date_format: str = DateFormat.YMD.value):
    """
    Validate a date string based on date format

    Args:
        date (str): date string to validate
        date_format (str): date format to validate against
    Returns:
        bool: True if valid, False otherwise
    Raises:
        ValueError: if date string is not valid for the given format

    """
    try:
        datetime.strptime(date, date_format)
    except ValueError:
        return False
    return True
