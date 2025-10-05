import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def user_data():
    return {"username": "testuser", "password": "testpass"}

def test_register_user(user_data):
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

def test_login_user(user_data):
    client.post("/auth/register", json=user_data)
    response = client.post("/auth/login", json=user_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
