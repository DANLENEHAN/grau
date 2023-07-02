from datetime import datetime
from enum import Enum
from typing import Annotated, Optional

from flask_login import UserMixin
from pydantic import BaseModel, EmailStr, HttpUrl, conint, constr, validator
from sqlalchemy import TIMESTAMP, Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from grau.db.enums import DateFormat, HeightUnits, WeightUnits
from grau.db.model import Base
from grau.utils import encrypt_str, validate_enum_member


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

    username: Annotated[
        str,
        constr(min_length=8, max_length=100, regex=r"^[A-Za-z0-9]+$"),
    ]
    email: EmailStr
    password: Annotated[
        str,
        constr(min_length=8, max_length=100, regex=r"^[A-Za-z0-9@#$%^&+=]+$"),
    ]

    status: str = UserStatus.ACTIVE.value
    profile_link: Optional[HttpUrl]
    premium: bool = False

    age: Annotated[int, conint(ge=0, le=150)]
    birthday: Annotated[str, constr(min_length=8, max_length=8)]
    first_name: Annotated[
        str, constr(min_length=8, max_length=50, regex=r"^[A-Za-z0-9]+$")
    ]
    last_name: Annotated[
        str, constr(min_length=8, max_length=50, regex=r"^[A-Za-z0-9]+$")
    ]
    gender: Annotated[str, constr(min_length=4, max_length=6)]

    phone_number: Annotated[int, conint(ge=99999999999999, le=999999999999999)]
    # https://countrycode.org/
    area_code: Annotated[str, constr(min_length=2, max_length=10)]
    height_unit_pref: Annotated[str, constr(min_length=2, max_length=2)]
    weight_unit_pref: Annotated[str, constr(min_length=3, max_length=2)]
    date_format_pref: Annotated[str, constr(min_length=8, max_length=11)]
    language: str

    _validate_birthday = validator("birthday", allow_reuse=True)(
        lambda birthday: datetime.strptime(birthday, DateFormat.YMD.value)
    )

    _validate_password = validator("password", allow_reuse=True)(
        lambda password: encrypt_str(secret_str=password)
    )

    _validate_height_unit = validator("height_unit_pref", allow_reuse=True)(
        lambda value: validate_enum_member(enum=HeightUnits, value=value)
    )

    _validate_weight_unit = validator("weight_unit_pref", allow_reuse=True)(
        lambda value: validate_enum_member(enum=WeightUnits, value=value)
    )

    _validate_date_format = validator("date_format_pref", allow_reuse=True)(
        lambda value: validate_enum_member(enum=DateFormat, value=value)
    )

    _validate_gender = validator("gender", allow_reuse=True)(
        lambda value: validate_enum_member(enum=Gender, value=value)
    )
