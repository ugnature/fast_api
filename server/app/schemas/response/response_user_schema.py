from pydantic import BaseModel
from datetime import datetime


class InstaUser(BaseModel):
    user_id: int
    user_email: str

    class Config:
        orm_mode = True


class newInstaUser(BaseModel):
    user_email: str
    user_created_at: datetime

    class Config:
        orm_mode = True


class updatedInstaUser(BaseModel):
    user_email: str
    user_updated_at: datetime

    class Config:
        orm_mode = True


class UserEmail(BaseModel):
    user_email: str

    class Config:
        orm_mode = True
