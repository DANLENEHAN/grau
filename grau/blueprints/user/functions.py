from grau.db.model import User
from sqlalchemy.orm import scoped_session


def create_user(session: scoped_session, user_dict: dict[str:str]) -> tuple[str, int]:
    user = User(**user_dict)

    if session.query(User).filter(User.email == user.email).one_or_none():
        return {"email": "email already assoicated with account"}, 400

    session.add(user)
    session.commit()
    return "User created successfully", 201
