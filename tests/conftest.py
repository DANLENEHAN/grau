"""
Pytest configuration file for test fixtures and plugins.

This `conftest.py` file is used to define common fixtures and configure plugins for pytest.
Fixtures are functions that provide reusable setup and teardown logic for tests.
Plugins extend the functionality of pytest and can be used to customize the test execution environment.

Fixtures defined in this file can be used by all tests in the same directory and subdirectories.
To use a fixture in a test, simply include it as an argument in the test function.


Fixtures defined here can also be overridden or extended in individual test modules or classes.

For more information on fixtures and plugins, refer to the pytest documentation: https://docs.pytest.org/en/latest/

"""

import os
import pytest
from unittest.mock import patch

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

import app as flask_app
from grau.db.model import Base


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with patch.dict(
        os.environ, {"APP_SECRET": "WDoxnMneVvbkb-VMAVNSDHDvEZjfjzrlPpLVQdYTQd0="}
    ):
        yield


@pytest.fixture(scope="module")
def session_factory():
    """
    The fixture is configured with scope="session", which means that the connection
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

    print("Tearing down database")
    # Teardown: Close the connection and clean up the database
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="module")
def db_session(session_factory):
    Session = scoped_session(session_factory)

    yield Session

    Session.remove()


@pytest.fixture(scope="module")
def app(session_factory):
    app = flask_app.create_app(session_factory=session_factory)

    yield app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
