from pydantic import BaseModel


class instaPostBaseModel(BaseModel):
    post_title: str
    post_content: str
    post_published: bool = True


class CreateInstaPostSM(instaPostBaseModel):
    pass

