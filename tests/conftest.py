"""
Pytest configuration file for test fixtures and plugins.

This `conftest.py` file is used to define common fixtures and configure plugins for pytest.
Fixtures are functions that provide reusable setup and teardown logic for tests.
Plugins extend the functionality of pytest and can be used to customize the test execution environment.

Fixtures defined in this file can be used by all tests in the same directory and subdirectories.
To use a fixture in a test, simply include it as an argument in the test function.


Fixtures defined here can also be overridden or extended in individual test modules or classes.

For more information on fixtures and plugins, refer to the pytest documentation: https://docs.pytest.org/en/latest/

There is duplication in the creation of the mock database session and api. There is db session and api client for both
a test by test scope and for a module scope. The module scopes are used more of itegration type testing where the order
of the tests matter and each one likely builds off the work of the last. These can not be run independantly. The
test by test scope shoulds be used for traditional unit test where you're testing a single function or small piece of
functionality at a time

"""

import os
from unittest.mock import patch

import pytest
from freezegun import freeze_time
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import app as flask_app
from grau.blueprints.user.functions import create_user
from grau.blueprints.user_stats.functions import create_user_stats
from grau.db.model import Base
from grau.db.user.user_model import User
from grau.db.user_stats.user_stats_model import UserStats
from grau.utils import decrypt_str


@pytest.fixture(scope="session", autouse=True)
def mock_settings_env_vars():
    """There's no reason for this salt to change"""
    with patch.dict(
        os.environ,
        {"APP_SECRET": "WDoxnMneVvbkb-VMAVNSDHDvEZjfjzrlPpLVQdYTQd0="},
    ):
        yield


@pytest.fixture(scope="function")
def function_session_factory():
    """
    The fixture is configured with scope="module", which means that the connection
    will be established once per test session and shared among all the tests.

    The `yield` statement separates the setup and teardown code.
    After yielding the connection, pytest executes the teardown code,
    which closes the connection and cleans up the database.
    """
    # Establish a connection to an in-memory SQLite database
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)

    yield session_factory

    # Teardown: Close the connection and clean up the database
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def function_db_session(function_session_factory):
    Session = scoped_session(function_session_factory)

    yield Session

    Session.remove()


@pytest.fixture(scope="function")
def function_app(function_session_factory):
    app = flask_app.create_app(session_factory=function_session_factory)

    yield app


@pytest.fixture(scope="function")
def function_client(function_app):
    """
    This is a fixture that can be used to test the api. It's a client that can be used to make requests to the api
    Scope: function - This means that the client will be created once per test function
    """
    return function_app.test_client()


@pytest.fixture(scope="class")
def class_session_factory():
    """
    The fixture is configured with scope="function", which means that the connection
    will be established once per test session and shared among all the tests.

    The `yield` statement separates the setup and teardown code.
    After yielding the connection, pytest executes the teardown code,
    which closes the connection and cleans up the database.
    """
    # Establish a connection to an in-memory SQLite database
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    session_factory = sessionmaker(bind=engine)

    yield session_factory

    # Teardown: Close the connection and clean up the database
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="class")
def class_db_session(class_session_factory):
    Session = scoped_session(class_session_factory)

    yield Session

    Session.remove()


@pytest.fixture(scope="class")
def class_app(class_session_factory):
    app = flask_app.create_app(session_factory=class_session_factory)

    yield app


@pytest.fixture(scope="class")
def class_client(class_app):
    return class_app.test_client()


@pytest.fixture(scope="function")
def insert_user_stat(function_db_session):
    """
    This is a fixture that can be used to insert a user stat into the database. It's a function that can be called to insert a user stat
    Scope: function - This means that the client will be created once per test function
    """

    def _insert_user_stat(user_stat):
        _, response_code = create_user_stats(function_db_session, user_stat)
        if response_code != 201:
            raise Exception(f"Failed to insert user: {user_stat}")
        return user_stat

    yield _insert_user_stat
    # Teardown: Erase all DB data after each test
    function_db_session.query(UserStats).delete()
    function_db_session.commit()


@pytest.fixture(scope="function")
def insert_user(function_db_session):
    """
    This is a fixture that can be used to insert a user into the database. It's a function that can be called to insert a user
    Scope: function - This means that the client will be created once per test function
    """

    def _insert_user(user):
        """
        This is a function that can be called to insert a user
        """
        _, response_code = create_user(function_db_session, user)
        if response_code != 201:
            raise Exception(f"Failed to insert user: {user}")
        return user

    yield _insert_user
    # Teardown: Erase all DB data after each test
    function_db_session.query(User).delete()
    function_db_session.commit()


@pytest.fixture()
def frozen_datetime():
    with freeze_time("2023-01-01"):
        yield


@pytest.fixture(scope="function")
def login_user(function_client):
    """
    This is a fixture that can be used to login a user. It's a function that can be called to login a user
    Scope: function - This means that the client will be created once per test function
    """

    def _login_user(user):
        """
        This is a function that can be called to login a user
        """
        response = function_client.post(
            "/login",
            json={
                "email": user["email"],
                "password": user["password"],
            },
        )
        if response.status_code != 200:
            raise Exception(f"Login failed: {response.status_code}")

    return _login_user
