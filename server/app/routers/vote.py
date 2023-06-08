from fastapi import Depends, status, HTTPException, APIRouter
from schemas.request.request_vote_schema import VoteSchema
from sqlalchemy.orm import Session
from database.database_connection.database import get_db
from database.db_models.models import voteDBTable, InstagramDBTableModel
from schemas.response import response_vote_schema
from routers import oauth2
from database.db_models import models
# this is going to give access to the function of COUNT which we will use to see join result
from sqlalchemy import func
from typing import List

router = APIRouter(prefix='/vote', tags=['Vote'])

# to get all the votes


@router.get('/', status_code=status.HTTP_302_FOUND, response_model=List[response_vote_schema.VoteSchema])
def votes(db: Session = Depends(get_db)):

    # this is extra function we created if we want to see total count of the votes
    results = db.query(models.InstagramDBTableModel, func.count(models.voteDBTable.vote_post_id).label('votes')).join(
        models.voteDBTable, models.voteDBTable.vote_post_id == models.InstagramDBTableModel.id, isouter=True).group_by(models.InstagramDBTableModel.id).all()
    print(results)
    return results


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote_schema: VoteSchema, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_insta_user)):

    # to check if the post exists in the database
    post = db.query(InstagramDBTableModel).filter(
        InstagramDBTableModel.id == vote_schema.vote_post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="this post does not exists")

    # before creating a vote we wanna see if the vote already exists, however this is not enough
    # cause multiple people can vate on a single post so just want to check with second condition
    # if the sameuser vote already exists or not in the database => db
    vote_query = db.query(voteDBTable).filter(voteDBTable.vote_post_id ==
                                              vote_schema.vote_post_id, voteDBTable.vote_user_id == current_user.user_id)
    found_vote = vote_query.first()
    if (vote_schema.direction_vote == 1):
        # if we found the data in our votetable in found_vote variable than he can't vote again
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.user_id} has already voted on the post {vote_schema.vote_post_id}')
        # if not found than we add the vote in the vote table
        new_vote = voteDBTable(
            vote_post_id=vote_schema.vote_post_id, vote_user_id=current_user.user_id)
        db.add(new_vote)
        db.commit()
        return {'massage': 'successfully added vote'}
    else:
        # if user want to delete the vote which he didn't wanted to vote but voted by mistake
        # before giving the permisson to delete we need to check if the vote already exists in the db or not of that user and if not than we raise exception cause we have already checked the database in above parameter
        # [16 line]

        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote doesn't exits")
        # now we know vote exists than we need to remove vote from the votetable of db
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'massage': 'successfully deleted vote'}
