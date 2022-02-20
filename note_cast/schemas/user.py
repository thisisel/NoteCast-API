import email
from datetime import datetime
from pydantic import BaseModel, EmailStr

class BaseUserPydantic(BaseModel):
    id : str
    username: str

class UserPydantic(BaseUserPydantic):
    email: EmailStr
    disabled : bool
    joined_date : datetime

