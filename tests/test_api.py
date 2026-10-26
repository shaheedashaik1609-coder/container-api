import os
from urllib import response
os.environ["API_KEY"] = "mysecretapikey"

from fastapi.testclient import TestClient
from app.main import app
from app.db import get_conn

#Replace with real db connection so these tests run without oracle
app.dependency_overrides[get_conn] = lambda: None

client = TestClient(app)
HEADERS = {"X-API-Key": "mysecretapikey"}

def test_health():
    response = client.get("/health", headers=HEADERS)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_missing_api_key_rejected():
    response = client.get("/containers/MSKU1234567")
    assert response.status_code == 401

def test_invalid_weight_rejected():
    response = client.post("/containers", headers=HEADERS, json={
        "container_id": "MSKU1234567",
        "size_ft": 20,
        "weight_kg": -1000,
        "destination": "New York",
        "status": "in_transit"
    })
    assert response.status_code == 422    

def test_predict_dwell():
    body = {"weight_kg": 20000, "is_40ft": 1, "arrival_hour": 14, "day_of_week": 2}
    response = client.post("/predict/dwell_time",json=body, headers=HEADERS)
    assert response.status_code == 200
    assert response.json() ["predicted_dwell_days"] > 0
    print("API response:", response.json())