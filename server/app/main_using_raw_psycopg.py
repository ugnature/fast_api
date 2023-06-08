from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# these are for sqlalchemy and one more which is from fastapi and that is Depends to start working with sqlalchemy


# here we created a connection with fastapi to this python script
app = FastAPI()


# here we created a connection with our postgres data base using psycopg2 plugin
# so we can send api request to our database to get the data
while True:
    try:
        connect = psycopg2.connect(host='localhost', database='...',
                                   user='...', password='...', cursor_factory=RealDictCursor)
        db_connection = connect.cursor()
        print('Database connection was successful!')
        break
    except Exception as error:
        print('Database connection was failed!')
        print('Error was: ', error)
        time.sleep(5)


# here we created our scheema a pydentic model
class PostModel(BaseModel):
    title: str
    content: str
    published: bool = True

# from here we started working on API, this fastapi is capable to work with postgres database veryfast


# to fetch all the post on instagram


@app.get('/posts')
def get_post():
    db_connection.execute("""SELECT * FROM instagram_posts""")
    instagram_posts = db_connection.fetchall()
    return {'data': instagram_posts}


# to create a new post on instagram
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post_scheema: PostModel):
    create_query = """INSERT INTO instagram_posts (post_title, post_content, post_published) VALUES (%s, %s, %s) RETURNING * """
    take_value_from = (post_scheema.title,
                       post_scheema.content, post_scheema.published)
    db_connection.execute(create_query, take_value_from)
    new_instagram_post = db_connection.fetchone()
    connect.commit()
    return {"data": new_instagram_post}


# to get a perticular post on instagram
@app.get('/posts/{id}')
def get_single_post(id: int, response: Response):
    find_query = """SELECT * FROM instagram_posts WHERE id = %s """
    # if u don't put "," after "str(id)" than u wouldn't be able to find a post which has double value is like 11, 34, 5667,
    take_value_from = str(id),
    db_connection.execute(find_query, take_value_from)
    instagram_single_post = db_connection.fetchone()
    print(instagram_single_post)
    if not instagram_single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"single_post_details": instagram_single_post}


# to delete a post on instagram
@app.delete("/posts/{id}")
def delete_post(id: int):
    delete_query = """DELETE FROM instagram_posts WHERE id = %s RETURNING *"""
    take_value_from = str(id),
    db_connection.execute(delete_query, take_value_from)
    connect.commit()
    deleted_insta_post = db_connection.fetchone()
    if deleted_insta_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This post does not exists")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# to update a post on instagram
@app.put("/posts/{id}")
def update_post(id: int, post_scheema: PostModel):
    update_post = """UPDATE instagram_posts SET post_title = %s, post_content = %s, post_published = %s WHERE id = %s RETURNING *"""
    take_value_from = (post_scheema.title,
                       post_scheema.content, post_scheema.published, str(id),)
    db_connection.execute(update_post, take_value_from)
    updated_post = db_connection.fetchone()
    connect.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with {id} doesn't exists")

    return {"data": updated_post}
