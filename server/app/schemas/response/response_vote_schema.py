from pydantic import BaseModel
from schemas.response.response_user_schema import UserEmail


class InstaPost(BaseModel):
    id: int
    user_key_id: int
    post_title: str
    post_content: str
    post_published: bool
    # here we added the scheema of what we want to show the to the user who is accessing this post


class VoteSchema(BaseModel):
    # Post: InstaPost
    votes: int

    class Config:
        orm_mode = True
