from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_extract_endpoint_demo_mode(monkeypatch):
    # Force Demo Mode so tests run deterministically offline
    monkeypatch.setenv("GEMINI_API_KEY", "demo")

    payload = {
        "raw_text": "Adults aged 18-75 with Type 2 Diabetes Mellitus and HbA1c between 7.5% and 10.5%."
    }
    response = client.post("/api/extract", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["min_age"] == 18
    assert data["max_age"] == 75
    assert "Type 2 Diabetes Mellitus" in data["primary_conditions"]
    assert "id" in data

def test_extract_rejects_short_input():
    response = client.post("/api/extract", json={"raw_text": "Too short"})
    assert response.status_code == 422
