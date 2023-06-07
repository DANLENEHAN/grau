from uuid import uuid4

from flask_login import login_user, logout_user
from sqlalchemy import and_
from sqlalchemy.orm import scoped_session

from grau.db.model import User
from grau.utils import encrypt_str, decrypt_str


def get_user(session: scoped_session, email: str) -> User:
    return session.query(User).filter(User.email == email).one_or_none()


def create_user(session: scoped_session, user_dict: dict[str:str]) -> tuple[str, int]:
    user_dict["password"] = encrypt_str(user_dict["password"])
    user = User(**user_dict)

    if get_user(session, user.email):
        return {"email": "email already assoicated with account"}, 400

    user.status = "active"
    session.add(user)
    session.commit()
    return "User created successfully", 201


def attempt_login(
    session: scoped_session, email: str, password: str
) -> tuple[str, int]:
    user = get_user(session, email)
    if user and decrypt_str(user.password) == password:
        user.session_id = str(uuid4())
        session.commit()
        login_user(user, remember=True)
        return "Login successful", 200
    return "Login failed, invalid credentials", 400


def attempt_logout(session: scoped_session, session_id: str) -> tuple[str, int]:
    user = (
        session.query(User)
        .filter(and_(User.session_id == decrypt_str(session_id)))
        .one_or_none()
    )
    if user:
        user.session_id = None
        session.commit()
        logout_user()
        return "Logout successful", 200
    return "Logout failed, invalid session", 400
