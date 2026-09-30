from fastapi.testclient import TestClient
import routes

from main import app


class FakeGenerator:
    def generate_document(self, document_type, parties, terms, dates):
        return (
            f"{document_type.upper()}\n\n"
            f"Parties: {parties}\n"
            f"Effective Date: {dates}\n\n"
            f"Terms: {terms}\n"
        )


def test_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "LegalEase API is running"


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate(monkeypatch):
    monkeypatch.setattr(routes, "generator", FakeGenerator())
    client = TestClient(app)

    response = client.post(
        "/generate",
        json={
            "document_type": "NDA",
            "parties": "Alice (Discloser), Bob (Recipient)",
            "terms": "Confidentiality; 30 day termination",
            "dates": "2026-09-28",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "NDA" in body["content"]
