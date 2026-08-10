from pydantic import BaseModel, Field

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