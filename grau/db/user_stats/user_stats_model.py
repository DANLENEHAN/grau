from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from grau.db.model import Base
from grau.db.user.user_model import User


class UserStats(Base):
    """
    User stats model for the database.
    """

    __tablename__ = "user_stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    value: Mapped[int] = mapped_column(Integer, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    note: Mapped[str] = mapped_column(String(100), nullable=True)

    user = relationship("User", back_populates="user_stats")

    def __repr__(self) -> str:
        return (
            f"UserStats(id={self.id!r},"
            "value={self.value!r}, unit={self.unit!r},"
            "created_at={self.created_at!r},"
            "updated_at={self.updated_at!r}, note={self.note!r})"
        )
