from fastapi import FastAPI, HTTPException
from app.models import TransactionResponse, TransactionCreate
from app.services import find_transaction, calculate_revenue, create_transaction as create_transaction_service


app = FastAPI(
    title = "Analytics Metrics API",
    version = '0.1.0',
)

@app.post("/transactions", response_model= TransactionResponse, status_code= 201)
def create_transaction(transaction: TransactionCreate):
    return create_transaction_service(country=transaction.country, revenue=transaction.revenue)


@app.get("/health")
def health():
    return{"status":"ok"}

@app.get("/metrics/revenue")
def get_revenue(country :str | None = None, min_revenue :float= 0):
    result = calculate_revenue(country = country, min_revenue= min_revenue)
    return {"metric": "revenue",
            "country": country.upper() if country else "ALL",
            "minimum_value": min_revenue,
            "value": result['total_revenue'],
            "currency": "EUR",
            "transaction_count" : result['transaction_count'],}

@app.get("/transactions/{transaction_id}", response_model= TransactionResponse,)
def get_transaction(transaction_id : int):
    transaction = find_transaction(transaction_id)
    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
    )
    return transaction