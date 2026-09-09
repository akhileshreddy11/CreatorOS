from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint_is_available_without_ai_key():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_dashboard_summary_exposes_safety_boundaries():
    response = client.get("/dashboard/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["safety"]["external_sends_require_approval"] is True
    assert payload["safety"]["payments_contracts_and_deletion_require_human"] is True
