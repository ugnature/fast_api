from pydantic import BaseModel, EmailStr
from typing import Optional


class InstaUserBaseModel(BaseModel):
    user_email: EmailStr
    user_password: str


class InstaUpdateUser(BaseModel):
    user_password: str


class UserLogin(BaseModel):
    user_email: EmailStr
    user_password: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
