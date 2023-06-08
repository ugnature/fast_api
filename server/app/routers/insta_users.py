from fastapi import Depends, status, Response, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
import utils
from schemas.request import request_user_schema
from schemas.response import response_user_schema
from database.database_connection.database import get_db
from database.db_models import models


router = APIRouter(
    prefix='/users',
    tags=['Instagram_Users']
)

# -----------------------------users api----------------------------------


# new user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=response_user_schema.newInstaUser)
def create_insta_user(user_scheema: request_user_schema.InstaUserBaseModel, db: Session = Depends(get_db)):
    # hash the password -> user_schema.user_password

    hashed_password = utils.hash(user_scheema.user_password)
    user_scheema.user_password = hashed_password
    new_insta_user = models.InstagramUserDBTabelModel(**user_scheema.dict())
    db.add(new_insta_user)
    db.commit()
    db.refresh(new_insta_user)
    return new_insta_user


# all users
@router.get('/', status_code=status.HTTP_302_FOUND, response_model=List[response_user_schema.InstaUser])
def insta_users(db: Session = Depends(get_db)):
    all_insta_users = db.query(models.InstagramUserDBTabelModel).all()
    return all_insta_users


# users by id
@router.get('/{id}', status_code=status.HTTP_302_FOUND, response_model=response_user_schema.InstaUser)
def insta_single_user(id: int, db: Session = Depends(get_db)):
    insta_user = db.query(models.InstagramUserDBTabelModel).filter(
        models.InstagramUserDBTabelModel.user_id == id).first()
    if not insta_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with this {id} is not registered with us!")
    return insta_user


# user_update
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=response_user_schema.updatedInstaUser)
def update_insta_user(id: int, user_scheema: request_user_schema.InstaUpdateUser, db: Session = Depends(get_db)):
    insta_user = db.query(models.InstagramUserDBTabelModel).filter(
        models.InstagramUserDBTabelModel.user_id == id)
    if insta_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with this id is not registered with us")
    hashed_password = utils.hash(user_scheema.user_password)
    user_scheema.user_password = hashed_password
    insta_user.update(user_scheema.dict(), synchronize_session=False)
    db.commit()
    return insta_user.first()


# delete_insta_user
@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_insta_user(id: int, db: Session = Depends(get_db)):
    insta_user = db.query(models.InstagramUserDBTabelModel).filter(
        models.InstagramUserDBTabelModel.user_id == id)
    if not insta_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'this user with id={id} is not registered with us!')
    insta_user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
