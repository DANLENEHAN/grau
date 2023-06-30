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
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import app as flask_app
from grau.db.model import Base


@pytest.fixture(scope="session", autouse=True)
def mock_settings_env_vars():
    """There's no reason for this salt to change"""
    with patch.dict(
        os.environ,
        {"APP_SECRET": "WDoxnMneVvbkb-VMAVNSDHDvEZjfjzrlPpLVQdYTQd0="},
    ):
        yield


@pytest.fixture(scope="module")
def module_session_factory():
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


@pytest.fixture(scope="module")
def module_db_session(module_session_factory):
    Session = scoped_session(module_session_factory)

    yield Session

    Session.remove()


@pytest.fixture(scope="module")
def module_app(module_db_session):
    app = flask_app.create_app(session_factory=module_db_session)

    yield app


@pytest.fixture(scope="module")
def module_client(module_app):
    return module_app.test_client()


@pytest.fixture(scope="function")
def session_factory():
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


@pytest.fixture(scope="function")
def db_session(session_factory):
    Session = scoped_session(session_factory)

    yield Session

    Session.remove()


@pytest.fixture(scope="function")
def app(session_factory):
    app = flask_app.create_app(session_factory=session_factory)

    yield app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()
