from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class UpdatePost(BaseModel):
    title: str
    content: str

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database is connected successfully")
        break
    except Exception as error:
        print("Connecting to database is failed")
        print(f"Error is: {error}")
        time.sleep(3)


@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/post/create", status_code=201)
def create_post(new_post: Post):
    # test sql-injection like pass values as f string
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (new_post.title, new_post.content, new_post.published))
    created_post = cursor.fetchone()
    conn.commit()
    return {"data": created_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    
    return Response(status_code=204)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")

    return {"data": updated_post}

# check put vs patch practically