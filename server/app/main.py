from fastapi import FastAPI
from database.database_connection.database import engine
from database.db_models import models
from routers import insta_posts, insta_users, vote
from routers import auth
from config import settings
from fastapi.middleware.cors import CORSMiddleware

# here we created a connection with fastapi to this python script

# don't need this command after alembic cause this commond helps sqlalchemy to manipulate database using fastapi but now we are using alembic to do that, meaning to create or delete db table or column
# values are not affected by this setup
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# to allow what domain should be able to talk to our api
# this middleware is so powerful, this gives us a freedom to choose what to allow and what to allow
# if other domain our using our api
# this middleware will work before sending any api request using any route

# -------- this origin below we define or gave permission to 2 website and if we want to give to everyone than
# origins = ["https://www.google.com", "https:www.youtube.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(insta_posts.router)
app.include_router(insta_users.router)
app.include_router(auth.router)
app.include_router(vote.router)
