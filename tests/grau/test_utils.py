"""
Test the grau.utils module.
"""
import os
from unittest.mock import MagicMock, patch

from grau.utils import decrypt_str, encrypt_str, get_secret_key


class TestUtils:
    """
    Test the grau.utils module.
    """

    app_secret: str = "XN-iJVBFzrohbtPhw6pVUh3CTsc14pV993uEhNUXVxw="
    test_password: str = "testing123"

    def test_get_secret_key(self):
        """
        Test that the function returns the APP_SECRET
        environment variable.
        """
        # given
        expected = self.app_secret
        os.environ["APP_SECRET"] = expected
        # when
        actual = get_secret_key()
        # then
        assert actual == expected

    def test_get_secret_key_none(self):  # noqa pylint: disable=R0201
        """
        Test that the function returns None if
        the APP_SECRET
        environment variable is not set.
        """
        # given
        del os.environ["APP_SECRET"]
        # when
        actual = get_secret_key()
        # then
        assert actual is None

    @patch("grau.utils.Fernet")
    def test_encrypt_str(self, mock_fernet: MagicMock):
        """
        Test that the function encrypts a string using a
        secret key.
        """
        # given
        secret_str = self.test_password
        # when
        encrypt_str(secret_str, self.app_secret)
        # then
        mock_fernet.assert_called_once_with(self.app_secret)
        encrypt = mock_fernet.return_value.encrypt
        encrypt.assert_called_once_with(secret_str.encode())
        encrypt.return_value.decode.assert_called_once()

    @patch("grau.utils.Fernet")
    def test_decrypt_str(self, mock_fernet: MagicMock):
        """
        Test that the function decrypts a string using a secret key.
        """
        # given
        secret_str = self.test_password
        # when
        decrypt_str(secret_str, self.app_secret)
        # then
        mock_fernet.assert_called_once_with(self.app_secret)

        decrypt = mock_fernet.return_value.decrypt
        decrypt.assert_called_once_with(secret_str.encode())
        decrypt.return_value.decode.assert_called_once()

    def test_decrypt_after_encrypt(self):
        """
        Test that the function decrypts a string
        after it was encrypted.
        """
        # given
        secret_str = self.test_password
        # when
        encrypted_str = encrypt_str(secret_str, self.app_secret)
        actual = decrypt_str(encrypted_str, self.app_secret)
        # then
        assert actual == secret_str
