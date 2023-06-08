from pydantic import BaseModel
from pydantic.types import conint

class VoteSchema(BaseModel):
    vote_post_id: int
    direction_vote: conint(le=1)