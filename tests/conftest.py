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

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from grau.db.model import Base


@pytest.fixture(scope="session")
def db_session():
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
    Session = scoped_session(session_factory)

    yield Session

    # Teardown: Close the connection and clean up the database
    Session.remove()


@pytest.fixture
def number():
    return 1
