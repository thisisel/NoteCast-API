import email
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class BaseUserPydantic(BaseModel):
    id: str
    username: str
    email: EmailStr


class UserPydantic(BaseUserPydantic):
    email: EmailStr
    disabled: bool
    joined_date: datetime


class UserInProfile(BaseUserPydantic):
    joined_date: datetime


class UserEdit(BaseUserPydantic):
    current_password: str = Field(...)
    new_password: str
