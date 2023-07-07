import os
from enum import Enum
from typing import Any, Optional, Type

from cryptography.fernet import Fernet


def get_secret_key() -> Optional[str]:
    """
    Returns the App secret key.
    Returns:
        str: secret key
    """
    return os.getenv("APP_SECRET")


def encrypt_str(secret_str: str, secret_key: Optional[str] = None) -> str:
    """
    Encrypts a string using a secret key.
    Args:
        secret_str (str): string to encrypt
        secret_key (str, optional): secret key to use for encryption.
                                    Defaults to None.
    Returns:
        str: encrypted string

    """
    if secret_key is None:
        secret_key = get_secret_key()
    f = Fernet(secret_key)
    return f.encrypt(secret_str.encode()).decode()


def decrypt_str(secret_str: str, secret_key: Optional[str] = None) -> str:
    """
    Decrypts a string using a secret key.

    Args:
        secret_str (str): encrypted string
        secret_key (Optional[str], optional): secret key. Defaults to None.

    Returns:
        str: decrypted string

    Raises:
        cryptography.fernet.InvalidToken: if the secret key is incorrect
    """
    if secret_key is None:
        secret_key = get_secret_key()
    f = Fernet(secret_key)
    return f.decrypt(secret_str.encode()).decode()


def validate_enum_member(enum: Type[Enum], value: Any) -> bool:
    """
    Validates if a value belongs to an Enum class.

    Args:
        enum (Enum): Enum class
        value (Any): value to validate
    Returns:
        bool: True if value belongs to Enum class, False otherwise
    """
    if value in [m.value for m in enum.__members__.values()]:
        return value
    raise ValueError(
        f"Value '{value}' does not belong to Enum class '{__name__}'"
    )
