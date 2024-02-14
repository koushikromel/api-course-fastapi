from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command

from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models


SQL_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"

engine = create_engine(SQL_DATABASE_URL)
# checking

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "koushik1@test.in", "password": "koushik"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "koushik2@test.in", "password": "koushik"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "Test Post 1",
            "content": "Test Post 1 Content",
            "owner_id": test_user["id"]
        },
        {
            "title": "Test Post 2",
            "content": "Test Post 2 Content",
            "owner_id": test_user["id"]
        },
        {
            "title": "Test Post 3",
            "content": "Test Post 3 Content",
            "owner_id": test_user["id"]
        },
        {
            "title": "Test Post 4",
            "content": "Test Post 4 Content",
            "owner_id": test_user2["id"]
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts = map(create_post_model, posts_data)
    session.add_all(posts)
    # session.add_all([
    #         models.Post(title="First Post", content="First content", owner_id=test_user["id"]), 
    #         models.Post(title="Second Post", content="Second content", owner_id=test_user["id"]), 
    #         models.Post(title="Third Post", content="Third content", owner_id=test_user["id"]), 
    # ])
    session.commit()

    posts = session.query(models.Post).all()
    return posts


