import pytest

from app import schemas
from .database import client, session


@pytest.fixture
def test_user(client):
    user_data = {"email": "koushik@test.in", "password": "koushik"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    return


# def test_root(client):
#     res = client.get("/")
#     # print(res.json().get("message"))
#     assert res.json().get("message") == "Hello, World!"
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "koushik@test.in", "password": "koushik"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "koushik@test.in"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": "koushik@test.in", "password": "koushik"})
    print(res.json())
    assert res.status_code == 200