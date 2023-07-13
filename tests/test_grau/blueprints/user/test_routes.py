"""
Tests the routes in the user blueprint
"""
from unittest.mock import ANY, MagicMock, patch


class TestRoutes:
    """
    Tests the routes in the user blueprint
    """

    @patch("grau.blueprints.user.routes.functions.create_user")
    def test_create_user(
        self, mock_create_user: MagicMock, client, user_factory
    ):
        """
        Tests the create_user route
        """
        # Given
        user = user_factory()
        # when
        client.post("/create_user", json=user)
        # Then
        mock_create_user.assert_called_once_with(ANY, user)

    @patch("grau.blueprints.user.routes.functions.attempt_login")
    def test_login(self, mock_attempt_login: MagicMock, client, user_factory):
        """
        Tests the login route
        """
        # Given
        user = user_factory()
        # when
        client.post(
            "/login",
            json={"email": user["email"], "password": user["password"]},
        )
        # Then
        mock_attempt_login.assert_called_once_with(
            ANY, user["email"], user["password"]
        )

    @patch("grau.blueprints.user.routes.functions.attempt_logout")
    @patch(
        "grau.blueprints.user.routes.session",
        MagicMock(get=MagicMock(return_value="testing123")),
    )
    def test_logout(
        self, mock_attempt_logout: MagicMock, client, user_factory
    ):
        """
        Tests the logout route
        """
        # Given
        user = user_factory()
        # when
        client.post("/logout", json={"email": user["email"]})
        # Then
        mock_attempt_logout.assert_called_once_with(ANY, "testing123")

    def test_test_auth(self, client, insert_user):
        """
        Tests the test_auth route
        """
        # Given
        insert_user()
        # when
        result = client.get("/user_authenticated")
        # Then
        assert result.status_code == 200
        assert result.data == b"User Authenticated"

    def test_test_auth_no_user(self, client):
        """
        Tests the test_auth route
        """
        # Given
        # when
        result = client.get("/user_authenticated")
        # Then
        assert result.status_code == 401
        assert result.data == (
            b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final'
            b'//EN">\n<title>'
            b"401 Unauthorized</title>\n<h1>"
            b"Unauthorized</h1>\n<p>The server could not "
            b"verify that you are authorized to access "
            b"the URL requested. You either "
            b"supplied the wrong credentials (e.g. a"
            b" bad password), or your browser doesn&#x27;t "
            b"understand how to supply the credentials required.</p>\n"
        )
