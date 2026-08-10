from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title = "Analytics Metrics API",
    version = '0.1.0',
)

transactions = [
    {"id": 1, "country": "DE", "revenue": 120.50},
    {"id": 2, "country": "DE", "revenue": 89.99},
    {"id": 3, "country": "FR", "revenue": 75.00},
    {"id": 4, "country": "UK", "revenue": 220.00},
    {"id": 5, "country": "FR", "revenue": 130.25},
]

class TransactionCreate(BaseModel):
    country: str = Field(
        min_length=2,
        max_length=2,
        description="Two-letter country code"
    )
    revenue: float = Field(gt=0, description=" The revenue must be greater than 0")

class TransactionResponse(BaseModel):
    id: int
    country: str
    revenue: float

@app.post("/transactions", response_model= TransactionResponse, status_code= 201)
def create_transaction(transaction: TransactionCreate):
    new_transaction = {
        "id": len(transactions) + 1,
        "country": transaction.country.upper(),
        "revenue": transaction.revenue,
    }

    transactions.append(new_transaction)

    return new_transaction

@app.get("/health")
def health():
    return{"status":"ok"}

@app.get("/metrics/revenue")
def get_revenue(country :str | None = None, min_revenue :float= 0):
    filtered_transactions = transactions
    if country is not None:
        filtered_transactions = [transaction
                                 for transaction in filtered_transactions
                                 if transaction["country"].upper() == country.upper()]

    
    if min_revenue > 0 :
        filtered_transactions = [transaction
                                 for transaction in filtered_transactions
                                 if transaction["revenue"] >= min_revenue]
          
    total_revenue = sum(transaction["revenue"] for transaction in filtered_transactions)
    return {"metric": "revenue",
            "country": country.upper() if country else "ALL",
            "minimum_value": min_revenue,
            "value": round(total_revenue, 2),
            "currency": "EUR",
            "transaction_count" : len(filtered_transactions),}

@app.get("/transactions/{transaction_id}", response_model= TransactionResponse,)
def get_transaction(transaction_id : int):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return transaction

    raise HTTPException(
        status_code=404,
        detail="Transaction not found"
    )