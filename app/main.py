from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class UpdatePost(BaseModel):
    title: str
    content: str

my_posts = [
    {"title": "title 1", "content": "Content of 1", "id": 1},
    {"title": "title 2", "content": "Content of 2", "id": 2},
    {"title": "title 3", "content": "Content of 3", "id": 3},
    {"title": "title 4", "content": "Content of 4", "id": 4},
]

def find_post(id):
    for post in my_posts:
        if post.get("id") == id:
            return post
    return {"error": "Not Found"}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        print(f"Index is {i} and post is {p}")
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/post/create", status_code=201)
def create_post(new_post: Post):
    post = new_post.model_dump()
    post['id'] = len(my_posts)+1
    my_posts.append(post)
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    print(status.HTTP_404_NOT_FOUND)
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    my_posts.pop(index)
    # return {"message": f"Deleted Post with id {id}"} # Avoid returning data when delete it leads to error instead do the following
    return Response(status_code=204)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=404, detail=f"Post with id: {id} not found")
    
    updated_post = post.model_dump()
    updated_post["id"] = id
    my_posts[index] = updated_post

    return {"data": updated_post}

# check put vs patch practically