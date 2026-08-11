from fastapi.testclient import TestClient
from app.main import app
from app.services import calculate_revenue

client = TestClient(app)


def test_transaction_count_starts_at_five():
    result = calculate_revenue()
    assert result["transaction_count"] == 5

def test_health():
    response = client.get("/health")

    assert response.status_code ==200
    assert response.json() == {"status":"ok"}

def test_get_transaction():
    response = client.get("/transactions/1")
    assert response.status_code == 200

def test_transaction_not_found():
    response = client.get("/transactions/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Transaction not found"}

def test_create_transaction():
    response = client.post("/transactions", json={
        "country": "de", "revenue": 150.0,
    },)
    created_transaction = response.json()

    transaction_id = created_transaction["id"]

    get_response = client.get(
        f"/transactions/{transaction_id}"
    )

    assert get_response.status_code == 200
    assert response.status_code == 201

def test_create_transaction_negative_revenue():
    response = client.post("/transactions", json={"country":"DE", "revenue":-100})
    assert response.status_code == 422

def test_create_transaction_missing_country():
    response = client.post("/transactions", json={"revenue":100})
    assert response.status_code == 422

