from fastapi.testclient import TestClient
from main import app
from model_name_enum import ModelName

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}

def test_read_user_me():
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"user_id": "the current user"}

def test_read_user():
    response = client.get("/users/testuser")
    assert response.status_code == 200
    assert response.json() == {"user_id": "testuser"}

def test_get_model():
    response = client.get(f"/models/{ModelName.cal}")
    assert response.status_code == 200
    assert response.json() == {"model_name": "cal", "message": "cal is caluculator`s cal"}

def test_read_item_with_query_params():
    response = client.get("/items/?skip=0&limit=1")
    assert response.status_code == 200
    assert response.json() == [{"item_name": "Foo"}]

def test_create_item():
    response = client.post("/items", json={"name": "test", "description": "test item", "price": 10.0, "is_offer": False})
    assert response.status_code == 200
    assert response.json() == {"name": "test", "description": "test item", "price": 10.0, "is_offer": False}