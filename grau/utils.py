import os

from cryptography.fernet import Fernet


def get_secret_key():
    """
    Returns the App secret key.
    """
    return os.getenv("APP_SECRET")


def encrypt_str(secret_str: str, secret_key: str = get_secret_key()) -> str:
    """
    Encrypts a string using a secret key.
    """
    f = Fernet(secret_key)
    return f.encrypt(secret_str.encode()).decode()


def decrypt_str(secret_str: str, secret_key: str = get_secret_key()) -> str:
    """
    Decrypts a string using a secret key.
    """
    f = Fernet(secret_key)
    return f.decrypt(secret_str.encode()).decode()
