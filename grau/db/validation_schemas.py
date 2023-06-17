from typing import Annotated

from pydantic import BaseModel, EmailStr, constr


class UserSchema(BaseModel):
    """
    Schema for validating user data
    """

    fullname: Annotated[str, constr(min_length=10, max_length=100, regex=r"^[A-Za-z]+\s[A-Za-z]+$")]
    email: EmailStr
    password: Annotated[str, constr(min_length=8, max_length=100, regex=r"^[A-Za-z0-9@#$%^&+=]+$")]
