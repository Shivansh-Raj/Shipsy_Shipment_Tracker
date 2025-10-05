import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def token():
    user_data = {"username": "Shivansh", "password": "1234"}
    client.post("/auth/register", json=user_data)
    log_in = client.post("/auth/login", json=user_data)
    return log_in.json()["access_token"]

def test_create_shipment(token):
    headers = {"Authorization": f"Bearer {token}"}
    shipment_data = {
        "description": "Test shipment",
        "weight": 5.0,
        "is_express": True,
        "status": "Pending"
    }
    response = client.post("/shipments/", json=shipment_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["description"] == "Test shipment"

def test_list_shipments(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/shipments/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
