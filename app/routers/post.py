from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)



# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=201, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # print('asdf', new_post)
    # print(type(new_post))
    print(current_user.email)
    print(current_user.id)
# {"title": "Never GiveUp", "content": "BE CONSISTENT", "published": True}
# curl -X POST -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNCwiZXhwIjoxNzAzOTkxMTQ3fQ.w5UOKw7B1xXDy50cT_SLhdcf4_hG7R6-sB4kX_P7DEk" -d "{\"title\": \"Never GiveUp\", \"content\": \"BE CONSISTENT\", \"published\": True}" http://localhost:8000/posts/create
    # created_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    created_post = models.Post(owner_id=current_user.id, **new_post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=403, detail=f"Not authorized to perform this logic")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to perform this logic")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to perform this logic")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()