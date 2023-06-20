from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated, Optional

from flask_login import UserMixin
from pydantic import BaseModel, EmailStr, HttpUrl, conint, constr, validator
from sqlalchemy import TIMESTAMP, Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from grau.db.enums import DateFormat, HeightUnits, TimestampFormat, WeightUnits
from grau.db.functions import datetime_to_string, validate_date_field
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

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
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
        return f"User(id={self.id!r}, fullname={self.fullname!r})"


class UserSchema(BaseModel):
    """
    Schema for validating user data
    """

    username: Annotated[
        str,
        constr(min_length=8, max_length=100, regex=r"^[A-Za-z0-9]+$"),
    ]
    email: EmailStr
    password: Annotated[
        str,
        constr(min_length=8, max_length=100, regex=r"^[A-Za-z0-9@#$%^&+=]+$"),
    ]

    created_at: timedelta = datetime_to_string(
        datetime.now(), date_format=TimestampFormat.YMD
    )
    updated_at: timedelta = datetime_to_string(
        datetime.now(), date_format=TimestampFormat.YMD
    )

    status: UserStatus = UserStatus.ACTIVE
    profile_link: HttpUrl
    premium: bool = False

    age: Annotated[int, conint(ge=0, le=150)]
    birthday: datetime
    first_name: Annotated[
        str, constr(min_length=8, max_length=50, regex=r"^[A-Za-z0-9]+$")
    ]
    last_name: Annotated[
        str, constr(min_length=8, max_length=50, regex=r"^[A-Za-z0-9]+$")
    ]
    gender: Gender

    phone_number: Annotated[int, conint(ge=99999999999999, le=999999999999999)]
    # https://countrycode.org/
    area_code: Annotated[str, constr(min_length=2, max_length=10)]
    height_unit_pref: HeightUnits
    weight_unit_pref: WeightUnits
    date_format_pref: DateFormat
    language: str

    _validate_birthday = validator("birthday", allow_reuse=True)(
        lambda birthday: validate_date_field(birthday, date_format=DateFormat.YMD)
    )
