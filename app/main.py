from fastapi import FastAPI, status, Response, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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


# check put vs patch practically

