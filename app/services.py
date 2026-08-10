from app.data import transactions


def find_transaction(transaction_id : int):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return transaction
    return None

def calculate_revenue(country :str | None = None, min_revenue :float= 0):
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
    return {"total_revenue": round(total_revenue, 2),
            "transaction_count" : len(filtered_transactions),}