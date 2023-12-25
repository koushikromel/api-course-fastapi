from fastapi import FastAPI, status, Response, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/post/create", status_code=201, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    print('asdf', new_post)
    print(type(new_post))

    # created_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    created_post = models.Post(**new_post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

# check put vs patch practically

@app.post("/users", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user