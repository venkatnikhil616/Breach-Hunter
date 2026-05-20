import pytest
from fastapi.testclient import TestClient

from app.api.app import create_app


client = TestClient(create_app())                 
                                                 
def test_root():
    response = client.get("/api/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
                                                  
def test_analyze_password():
    payload = {"password": "Test123!"}
    response = client.post("/api/analyze", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "strength" in data
    assert "feedback" in data
    assert "breached" in data


def test_analyze_weak_password():                     payload = {"password": "12345"}
    response = client.post("/api/analyze", json=payload)
                                                      assert response.status_code == 200
    data = response.json()

    assert data["strength"]["strength"] in ["Weak", "Moderate"]

                                                  def test_invalid_request():
    payload = {}  # missing password
    response = client.post("/api/analyze", json=payload)

    assert response.status_code == 422
