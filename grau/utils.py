import os
from enum import Enum
from typing import Any, Optional

from cryptography.fernet import Fernet


def get_secret_key():
    """
    Returns the App secret key.
    """
    return os.getenv("APP_SECRET")


def encrypt_str(secret_str: str, secret_key: Optional[str] = None) -> str:
    """
    Encrypts a string using a secret key.
    """
    if secret_key is None:
        secret_key = get_secret_key()
    f = Fernet(secret_key)
    return f.encrypt(secret_str.encode()).decode()


def decrypt_str(secret_str: str, secret_key: Optional[str] = None) -> str:
    """
    Decrypts a string using a secret key.
    """
    if secret_key is None:
        secret_key = get_secret_key()
    f = Fernet(secret_key)
    return f.decrypt(secret_str.encode()).decode()


def validate_enum_member(enum: type[Enum], value: Any) -> bool:
    """
    Validate that a value belongs to an Enum class.
    """

    if value in [m.value for m in enum.__members__.values()]:
        return value
    raise ValueError(
        f"Value '{value}' does not belong to Enum class '{__name__}'"
    )
