from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from datetime import datetime, timedelta
from schemas.request.request_user_schema import TokenData, Token
from routers import auth
from database.database_connection.database import get_db
from database.db_models import models
from sqlalchemy.orm import Session
from config import settings

oAuth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# algorithm
# Expiration Time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


# this verify access token is stablished here after setting up auth route and from there i got this "user_id"
# payload and than i am going to varify that token which we created there in auth.py with new regeneration
# of the token of same id so we can do matching of jwt token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms={ALGORITHM})
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWSError:
        raise credentials_exception

    return token_data


def get_current_insta_user(token: str = Depends(oAuth2_schema), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(
        token, credentials_exception=credential_exception)
    insta_user = db.query(models.InstagramUserDBTabelModel).filter(
        models.InstagramUserDBTabelModel.user_id == token.id).first()
    print(insta_user)
    return insta_user
