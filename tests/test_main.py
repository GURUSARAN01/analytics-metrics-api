from fastapi.testclient import TestClient
from app.main import app, transactions
import pytest

client = TestClient(app)

original_transactions = [transaction.copy() for transaction in transactions]

@pytest.fixture(autouse=True)
def reset_transactions():
    transactions.clear()
    transactions.extend(
        transaction.copy()
        for transaction in original_transactions
   )
    yield

    transactions.clear()

    transactions.extend(
        transaction.copy()
        for transaction in original_transactions
    )
def test_transaction_count_starts_at_five():
    assert len(transactions) == 5

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
    assert response.status_code == 201

def test_create_transaction_negative_revenue():
    response = client.post("/transactions", json={"country":"DE", "revenue":-100})
    assert response.status_code == 422

def test_create_transaction_missing_country():
    response = client.post("/transactions", json={"revenue":100})
    assert response.status_code == 422

