from fastapi import FastAPI, status, Response, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

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

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/post/create", status_code=201)
def create_post(new_post: Post, db: Session = Depends(get_db)):
    # created_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    created_post = models.Post(**new_post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return {"data": created_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}

# check put vs patch practically