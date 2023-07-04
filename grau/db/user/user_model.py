from datetime import datetime
from enum import Enum
from typing import Optional

from flask_login import UserMixin
from pydantic import BaseModel, EmailStr, Field, HttpUrl, validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import TIMESTAMP, Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from grau.db.enums import DateFormat, HeightUnits, WeightUnits
from grau.db.model import Base
from grau.utils import encrypt_str


class UserStatus(Enum):
    """
    Enum for user status
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"
    BANNED = "banned"


class Gender(Enum):
    """
    Enum for user gender
    """

    MALE = "male"
    FEMALE = "female"


class User(UserMixin, Base):
    """
    User model for the database.
    """

    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()  # pylint: disable=E1102
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),  # pylint: disable=E1102
        onupdate=func.now(),  # pylint: disable=E1102
    )
    session_id: Mapped[str] = mapped_column(String(150), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=True)
    profile_link: Mapped[str] = mapped_column(String(100), nullable=True)
    premium: Mapped[bool] = mapped_column(Boolean, nullable=True)

    age: Mapped[int] = mapped_column(Integer, nullable=True)
    birthday: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True)
    area_code: Mapped[str] = mapped_column(String(20), nullable=True)
    height_unit_pref: Mapped[str] = mapped_column(String(50), nullable=True)
    weight_unit_pref: Mapped[str] = mapped_column(String(50), nullable=True)
    date_format_pref: Mapped[str] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=True)

    def get_id(self) -> str:
        """_summary_
        We encrypt the session ID so that it is not leaked to the client.
        Returns:
            str: encrypted session ID"""

        return encrypt_str(str(self.session_id))

    def __repr__(self) -> str:
        return f"(Name={self.first_name!r})"


class UserValidationSchema(BaseModel):
    """
    Schema for validating user data
    """

    username: str = Field(
        min_length=8, max_length=100, pattern=r"^[A-Za-z0-9]+$"
    )

    email: EmailStr
    password: str = Field(
        min_length=8, max_length=100, pattern=r"^[A-Za-z0-9@#$%^&+=]+$"
    )

    status: UserStatus = Field(default=UserStatus.ACTIVE.value)
    profile_link: HttpUrl | None = None
    premium: bool = Field(default=False)

    age: int = Field(ge=0, le=150)
    birthday: str = Field(min_length=10, max_length=10)
    first_name: str = Field(
        min_length=3, max_length=50, pattern=r"^[A-Za-z0-9]+$"
    )
    last_name: str = Field(
        min_length=3, max_length=50, pattern=r"^[A-Za-z0-9]+$"
    )
    gender: Gender

    phone_number: PhoneNumber
    area_code: str = Field(min_length=2, max_length=10)
    height_unit_pref: HeightUnits
    weight_unit_pref: WeightUnits
    date_format_pref: DateFormat
    language: str

    _validate_birthday = validator("birthday", allow_reuse=True)(
        lambda birthday: datetime.strptime(birthday, DateFormat.YMD.value)
    )

    _validate_password = validator("password", allow_reuse=True)(
        lambda password: encrypt_str(secret_str=password)
    )

    class Config:
        """
        Pydantic config class
        """

        use_enum_values = True
