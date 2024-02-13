from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command


from app import schemas
from app.main import app
from app.config import settings
from app.database import get_db, Base



SQL_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"

engine = create_engine(SQL_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    # run our code before we run our test
    # command.downgrade("head") # using alembic
    # command.upgrade("head") #using alembic
    yield TestClient(app)
    # run our code after we run our test


def test_root(client):
    res = client.get("/")
    # print(res.json().get("message"))
    assert res.json().get("message") == "Hello, World!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "koushik@test.in", "password": "koushik"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "koushik@test.in"
    assert res.status_code == 201

