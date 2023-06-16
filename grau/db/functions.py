import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


def get_db_engine() -> Engine:
    db_url = os.environ.get("DATABASE_URL")
    db_url = db_url or "postgresql+psycopg2://dan:testing123@localhost/train"
    return create_engine(db_url)


def get_session_maker() -> sessionmaker:
    return sessionmaker(bind=get_db_engine())
