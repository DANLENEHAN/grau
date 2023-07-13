"""
Tests the functions in the user blueprint
"""
from unittest.mock import MagicMock, patch

import pytest

from grau.blueprints.user import functions
from grau.exceptions.grau_exceptions import ResourceAlreadyExists
from grau.utils import decrypt_str


class TestFunctions:
    """
    Tests the functions in the user blueprint
    """

    def test_get_user(self, db_session, insert_user, db_class_comparison):
        """
        Tests get_user function
        """
        # Given
        test_user = insert_user()

        # when
        result = functions.get_user(db_session, email=test_user.email)
        # Then
        db_class_comparison(result, test_user)

    def test_get_user_no_user(self, db_session):
        """
        Tests get_user function
        """
        # Given
        # when
        result = functions.get_user(db_session, email="fake_email@email.com")
        # Then
        assert result is None

    def test_create_user(self, db_session, user_factory):
        """
        Tests the create_user function
        """
        # Given
        user = user_factory()
        # when
        result = functions.create_user(
            db_session=db_session, user_dict=user.copy()
        )
        # Then
        assert result == ("User created successfully", 201)

    def test_create_user_already_exists(
        self, db_session, insert_user, user_factory
    ):
        """
        Tests the user session management capabilities
        """
        # Given
        user = user_factory()
        insert_user(user)
        # When
        with pytest.raises(ResourceAlreadyExists) as excinfo:
            functions.create_user(db_session=db_session, user_dict=user.copy())
        # Then
        assert "Email already assoicated with account" in str(excinfo.value)

    @patch("grau.blueprints.user.functions.login_user", MagicMock())
    def test_attempt_login(self, db_session, insert_user):
        """
        Tests the user session management capabilities
        """
        # Given
        test_user = insert_user()
        # When
        result = functions.attempt_login(
            db_session=db_session,
            email=test_user.email,
            password=decrypt_str(test_user.password),
        )
        # Then
        assert result == ("Login successful", 200)

    def test_attempt_login_no_user(self, db_session, user_factory):
        """
        Tests the attempt_login function when no such user exists
        """

        # Given
        user = user_factory()
        # When
        result = functions.attempt_login(
            db_session=db_session,
            email=user["email"],
            password=user["password"],
        )
        # Then
        assert result == ("Login failed, invalid credentials", 400)

    # TODO: Fix this test, it is failing due to a misisng
    # session_id for the create user even after login

    # @patch("grau.blueprints.user.functions.logout_user", MagicMock())
    # def test_attempt_logout(self, db_session, insert_user):
    #     """
    #     Tests the attempt_logout function when user exists
    #     """
    #     # Given
    #     test_user = insert_user(login=True)

    #     # When
    #     result = functions.attempt_logout(
    #         db_session=db_session,
    #         session_id=test_user.session_id,
    #     )
    #     # Then
    #     assert result == ("Logout successful", 200)

    def test_attempt_logout_no_user(self, db_session):
        """
        Tests the attempt_logout function when no such user exists
        """

        # Given
        # When
        result = functions.attempt_logout(
            db_session=db_session,
            session_id=None,
        )
        # Then
        assert result == ("Logout failed, user not logged in", 400)
