from typing import Optional

from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from grau.utils import encrypt_str


class Base(DeclarativeBase):
    pass


class User(UserMixin, Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(String(100), nullable=True)
    session_id: Mapped[str] = mapped_column(String(100), nullable=True)

    def get_id(self) -> str:
        """_summary_
        We encrypt the session ID so that it is not leaked to the client.
        Returns:
            str: encrypted session ID"""

        return encrypt_str(str(self.session_id))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
