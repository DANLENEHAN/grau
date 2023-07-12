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
from typing import Any, Dict, Generator, Optional
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


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    """
    There's no reason for this salt to change
    There must be a class level var for
    the test classes to pick up the fixture
    """
    with patch.dict(
        os.environ,
        {"APP_SECRET": "WDoxnMneVvbkb-VMAVNSDHDvEZjfjzrlPpLVQdYTQd0="},
    ):
        yield


@pytest.fixture()
def session_factory():
    """
    The fixture is configured with scope="function", which means that the connection
    will be established once per test.

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


@pytest.fixture()
def db_session(session_factory):
    Session = scoped_session(session_factory)

    yield Session

    Session.remove()


@pytest.fixture()
def app(session_factory):
    app = flask_app.create_app(session_factory=session_factory)
    yield app


@pytest.fixture()
def insert_user_stat(db_session, user_stats_factory):
    """
    This is a fixture that can be used to insert a user stat into the database. It's a function that can be called to insert a user stat
    Scope: function - This means that the client will be created once per test function
    """

    def _insert_user_stat(
        user_stat: Optional[Dict] = None, user_id: Optional[int] = None
    ):
        if user_stat is None:
            user_stat = user_stats_factory(user_id=user_id)

        _, response_code = create_user_stats(db_session, user_stat)
        if response_code != 201:
            raise Exception(f"Failed to insert user: {user_stat}")
        # Get last user stat added to the db
        user_stat = (
            db_session.query(UserStats)
            .filter(UserStats.user_id == user_stat["user_id"])
            .order_by(UserStats.id.desc())
            .first()
        )
        return user_stat

    yield _insert_user_stat
    # Teardown: Erase all DB data after each test
    db_session.query(UserStats).delete()
    db_session.commit()


@pytest.fixture()
def insert_user(db_session, user_factory, login_user):
    """
    This is a fixture that can be used to insert a user into the database. It's a function that can be called to insert a user
    Scope: function - This means that the client will be created once per test function
    """

    def _insert_user(user: Optional[Dict] = None, login: bool = True):
        """
        This is a function that can be called to insert a user

        Args:
            user: The user to insert. If None, a user will be created using the user_factory
            login: If True, the user will be logged in after being created

        Returns:
            The user that was inserted

        Raises:
            Exception: If the user was not inserted successfully
        """
        if user is None:
            user = user_factory()
        _, response_code = create_user(db_session, user)
        if response_code != 201:
            raise Exception(f"Failed to insert user: {user}")
        user = (
            db_session.query(User).filter(User.email == user["email"]).first()
        )
        if login:
            login_user(user)
        return user

    yield _insert_user
    # Teardown: Erase all DB data after each test
    db_session.query(User).delete()
    db_session.commit()


@pytest.fixture()
def frozen_datetime():
    with freeze_time("2023-01-01"):
        yield


@pytest.fixture()
def login_user(client):
    """
    This is a fixture that can be used to login a user. It's a function that can be called to login a user
    Scope: function - This means that the client will be created once per test function
    """

    def _login_user(user):
        """
        This is a function that can be called to login a user
        """
        response = client.post(
            "/login",
            json={"email": user.email, "password": decrypt_str(user.password)},
        )
        if response.status_code != 200:
            raise Exception(f"Login failed: {response.status_code}")

    return _login_user


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def test_integration(client):
    def _run_integration_tests(test_cases):
        for test_case in test_cases:
            test_case = test_case.to_dict()
            if test_case["method"] == "POST":
                response = client.post(
                    test_case["endpoint"], json=test_case["payload"]
                )
            elif test_case["method"] == "GET":
                response = client.get(
                    test_case["endpoint"], json=test_case["payload"]
                )
            elif test_case["method"] == "PUT":
                response = client.put(
                    test_case["endpoint"], json=test_case["payload"]
                )

            assert response.status_code == test_case["expected_response_code"]
            assert response.data == test_case["expected_response"]

    return _run_integration_tests


@pytest.fixture
def user_factory():
    def _create_user(**kwargs) -> Dict:
        user = {
            "age": 25,
            "area_code": "353",
            "birthday": "1997-05-18",
            "date_format_pref": "%d-%m-%Y",
            "email": "dan@trainai.com",
            "first_name": "Dan",
            "gender": "male",
            "height_unit_pref": "cm",
            "language": "english",
            "last_name": "lenehan",
            "password": "testing123",
            "phone_number": "+1 202-918-2132",
            "username": "danlen97",
            "weight_unit_pref": "kg",
        }

        # Update the user dictionary with any keyword arguments passed in
        user.update(kwargs)

        return user

    return _create_user


@pytest.fixture
def user_stats_factory():
    def _create_user_stat(user_id: int, **kwargs) -> Dict:
        """
        Returns a user stats dictionary.
        """
        user_stat = {
            "user_id": user_id,
            "value": 1,
            "unit": "kg",
            "note": "this note is a nice note",
        }
        user_stat.update(kwargs)
        return user_stat

    return _create_user_stat
