"""
Integration scenarios testing user login, logout
and session handling capabilities
"""
from typing import Dict, Union


class IntegrationTestStep:
    """
    This class represents a single step in an integration test
    """

    def __init__(  # noqa pylint: disable=R0913
        self,
        endpoint: str,
        payload: Dict,
        expected_response: Union[Dict, str, bytes],
        expected_response_code: int,
        method: str,
    ):
        self.endpoint = endpoint
        self.payload = payload
        self.expected_response = expected_response
        self.expected_response_code = expected_response_code
        self.method = method

    def to_dict(self) -> Dict:
        """
        Returns a dictionary representation of the test step
        """
        return {
            "endpoint": self.endpoint,
            "payload": self.payload,
            "expected_response": self.expected_response,
            "expected_response_code": self.expected_response_code,
            "method": self.method,
        }


class TestUserSessionIntegration:
    """
    Tests the user session handling capabilities
    """

    successful_auth_step = IntegrationTestStep(
        endpoint="/user_authenticated",
        payload={},
        expected_response=b"User Authenticated",
        expected_response_code=200,
        method="GET",
    )

    unsuccessful_auth_step = IntegrationTestStep(
        endpoint="/user_authenticated",
        payload={},
        expected_response=(
            b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final'
            b'//EN">\n<title>'
            b"401 Unauthorized</title>\n<h1>"
            b"Unauthorized</h1>\n<p>The server could not "
            b"verify that you are authorized to access "
            b"the URL requested. You either "
            b"supplied the wrong credentials (e.g. a"
            b" bad password), or your browser doesn&#x27;t "
            b"understand how to supply the credentials required.</p>\n"
        ),
        expected_response_code=401,
        method="GET",
    )

    @staticmethod
    def create_user_step(test_user: Dict, successful: bool = True):
        """
        Returns a test step for creating a user
        """
        return IntegrationTestStep(
            endpoint="/create_user",
            payload=test_user,
            expected_response=b"User created successfully"
            if successful
            else (
                b'{"data":null,"message":'
                b'"Email already assoicated with account"}\n'
            ),
            expected_response_code=201 if successful else 409,
            method="POST",
        )

    logout_step = IntegrationTestStep(
        endpoint="/logout",
        payload={"session_id": "testing123"},
        expected_response=b"Logout successful",
        expected_response_code=200,
        method="POST",
    )

    @staticmethod
    def login_step(test_user: Dict, successful: bool = True):
        """
        Returns a test step for logging in a user
        """
        return IntegrationTestStep(
            endpoint="/login",
            payload={
                "email": test_user["email"],
                "password": test_user["password"],
            },
            expected_response=b"Login successful"
            if successful
            else b"Login failed, invalid credentials",
            expected_response_code=200 if successful else 400,
            method="POST",
        )

    def test_user_session_management_happy_path(
        self, test_integration, user_factory
    ):
        """
        Tests the user session management capabilities
        """
        # Given
        test_user = user_factory()
        test_cases = [
            self.create_user_step(test_user=test_user),
            self.login_step(test_user=test_user),
            self.successful_auth_step,
            self.logout_step,
            self.unsuccessful_auth_step,
        ]
        # Then
        test_integration(test_cases)

    def test_user_session_management_no_user(
        self, test_integration, user_factory
    ):
        """
        Tests the user session management capabilities
        """
        # Given
        test_cases = [
            self.login_step(test_user=user_factory(), successful=False),
            self.unsuccessful_auth_step,
        ]
        # Then
        test_integration(test_cases)

    def test_user_double_create(self, test_integration, user_factory):
        """
        Tests the user session management capabilities
        """
        # Given
        test_user = user_factory()
        test_cases = [
            self.create_user_step(test_user=test_user.copy()),
            # Try to create the same user again
            self.create_user_step(
                test_user=test_user.copy(), successful=False
            ),
        ]
        # Then
        test_integration(test_cases)
