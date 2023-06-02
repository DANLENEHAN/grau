from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


def get_session_factory():
    """
    When the app is created the Session registry is established.
    The Session registry is a dictionary that maps the thread id to the
    Session object.
    """
    engine = create_engine("postgresql+psycopg2://dan:testing123@localhost/train")
    return sessionmaker(bind=engine)
