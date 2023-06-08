from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.database_connection.database import get_db
from schemas.request import request_user_schema
from database.db_models import models
import utils
from routers import oauth2


router = APIRouter(tags=['Authentication'])

#  here we just created jwt token for every user


@router.post('/login', status_code=status.HTTP_200_OK, response_model=request_user_schema.Token)
def auth(user_auth_schema: request_user_schema.UserLogin, db: Session = Depends(get_db)):
    auth_user = db.query(models.InstagramUserDBTabelModel).filter(
        models.InstagramUserDBTabelModel.user_email == user_auth_schema.user_email).first()
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    if not utils.verify(user_auth_schema.user_password, auth_user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(
        data={"user_id": auth_user.user_id})
    # return token
    return {"access_token": access_token, "token_type": "bearer"}

# --------this function has OAuth2PasswordRequestFrom----------------------------------------nothing else-----all are same---------------

# @router.post('/login')
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     auth_user = db.query(models.InstagramUserDBTabelModel).filter(
#         models.InstagramUserDBTabelModel.user_email == user_credentials.username).first()
#     if not auth_user:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
#     if not utils.verify(user_credentials.password, auth_user.user_password):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

#     # create a token
#     # return token
#     access_token = oauth2.create_access_token(
#         data={"user_id": auth_user.user_id})
#     return {"access_token": access_token, 'token_type': "bearer"}
