import pytest
from jose import jwt

from app import schemas
from app.config import settings


# def test_root(client):
#     res = client.get("/")
#     assert res.json().get("message") == "Hello, World!"
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "koushik@test.in", "password": "koushik"})
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "koushik@test.in"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email ,password, status_code", [
    ("koushik@test.in", "koushika", 403),
    ("koushik1@test.in", "koushika", 403),
    (None, "koushika", 422),
    ("koushik1@test.in", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == detail

