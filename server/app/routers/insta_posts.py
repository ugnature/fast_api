from fastapi import Depends, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.request import request_post_schemas
from schemas.response import response_post_schemas
from database.db_models import models
from database.database_connection.database import get_db
from routers import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Instagram_Posts']
)

# --------------------------------posts api---------------------------------------

# to fetch all the post on instagram


@router.get('/', status_code=status.HTTP_302_FOUND, response_model=List[response_post_schemas.InstaPost])
def get_post(db: Session = Depends(get_db)):
    all_insta_post = db.query(models.InstagramDBTableModel).all()
    result = db.query(models.InstagramDBTableModel)
    print(result)
    return all_insta_post


# ------------we can add a new feature here in this api--- let's say we want to retrieve last 5 post only
# ------- so we need to add query parameter in the above api--- i create a copy down below to make some changes
# ----- this query parameter will be after the depends(get_db)
@router.get('/search', status_code=status.HTTP_302_FOUND, response_model=List[response_post_schemas.InstaPost])
# here we just added limit varible
# we can add one more feature of skiping some post lets say first few , so we use offset parameter
# we can also add the feature of search with the title of the post
def get_post(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, title: Optional[str] = ""):
    # we just added limit query parameter in our sqlAlchemy
    # now this filter feature will help us in finding post based on the title
    # offset help us skiping posts
    all_insta_post = db.query(models.InstagramDBTableModel).filter(models.InstagramDBTableModel.post_title.contains(title)).limit(
        limit).offset(skip).all()
    return all_insta_post


# --------------------------an extra feature to create the personal access-----------------------------

# this getting all the post can be private also meaning the user who created it can only see his all the post


@router.get('/auth', status_code=status.HTTP_302_FOUND, response_model=List[response_post_schemas.InstaPost])
def get_post(db: Session = Depends(get_db), current_insta_user: int = Depends(oauth2.get_current_insta_user)):
    all_insta_post = db.query(models.InstagramDBTableModel).filter(
        models.InstagramDBTableModel.user_key_id == current_insta_user.user_id).all()
    if not all_insta_post:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you don't have access to this post")
    print(all_insta_post)
    return all_insta_post

# ------------------------------------------------end---------------------------------------------------------

# to create a new post on instagram


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=response_post_schemas.CreatedInstaPost)
def create_posts(post_scheema: request_post_schemas.CreateInstaPostSM, db: Session = Depends(get_db), current_insta_user: int = Depends(oauth2.get_current_insta_user)):
    # here we added the user_key_id in the post through the jwt token in the new_instagram_post
    print(current_insta_user.user_id)
    new_instagram_post = models.InstagramDBTableModel(
        user_key_id=current_insta_user.user_id, **post_scheema.dict())
    db.add(new_instagram_post)
    db.commit()
    db.refresh(new_instagram_post)
    return new_instagram_post


# to get a perticular post on instagram
@router.get('/{id}', status_code=status.HTTP_302_FOUND, response_model=response_post_schemas.InstaPost)
def get_single_post(id: int, db: Session = Depends(get_db), current_insta_user: int = Depends(oauth2.get_current_insta_user)):
    instagram_single_post = db.query(models.InstagramDBTableModel).filter(
        models.InstagramDBTableModel.id == id).first()
    if not instagram_single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return instagram_single_post


# to delete a post on instagram
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_insta_user: int = Depends(oauth2.get_current_insta_user)):
    # this is just the db access with that id
    insta_single_post_query = db.query(models.InstagramDBTableModel).filter(
        models.InstagramDBTableModel.id == id)
    insta_single_post = insta_single_post_query.first()
    # here we just checking if post exsist of that id or not
    if insta_single_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This post does not exists")
    # here we just added the logic of if the current_insta_user.user_id == to the user_key_id of the post
    if insta_single_post.user_key_id != current_insta_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    # otherwise now perform the action on that post
    insta_single_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# to update a post on instagram
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=response_post_schemas.UpdatedInstaPost)
def update_post(id: int, post_scheema: request_post_schemas.CreateInstaPostSM, db: Session = Depends(get_db), current_insta_user: int = Depends(oauth2.get_current_insta_user)):
    # here we are porforming query to find a post of that id
    insta_single_post_query = db.query(models.InstagramDBTableModel).filter(
        models.InstagramDBTableModel.id == id)
    # if we are able to find that id of the post than we assign this value to new variable
    insta_single_post = insta_single_post_query.first()
    # if we are not able to find that id of the post in the our database table of post_table than throw exception
    if insta_single_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with {id} doesn't exists")
    # otherwise now check if the current_insta_user.user_id == to the post user_key_id, so we give permisson to
    # the rightuser to update the post
    if insta_single_post.user_key_id != current_insta_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    # if yes, than perfrom this action below
    insta_single_post_query.update(
        post_scheema.dict(), synchronize_session=False)
    db.commit()
    return insta_single_post
