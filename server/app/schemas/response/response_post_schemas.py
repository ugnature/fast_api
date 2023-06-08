from pydantic import BaseModel
from datetime import datetime
from schemas.response.response_user_schema import UserEmail


class InstaPost(BaseModel):
    id: int
    user_key_id: int
    post_title: str
    post_content: str
    post_published: bool
    # here we added the scheema of what we want to show the to the user who is accessing this post
    owner: UserEmail

    class Config:
        orm_mode = True


class CreatedInstaPost(InstaPost):
    post_created_at: datetime


class UpdatedInstaPost(InstaPost):
    id: int
    post_created_at: datetime
    user_key_id: int
