from app.database import get_connection


def find_transaction(transaction_id : int):
    connection = get_connection()
    row = connection.execute(
        """SELECT id, country, revenue
        FROM transactions 
        WHERE id = ?""", (transaction_id,),
    ).fetchone()
    connection.close()
    if row is None:
        return None
    return dict(row)
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return transaction
    return None

def calculate_revenue(country :str | None = None, min_revenue :float= 0):
    connection = get_connection()
    query = """SELECT COALESCE(SUM(revenue),0) AS total_revenue,
    COUNT(*) AS transaction_count
    FROM transactions
    WHERE revenue >= ?"""
    parameters = [min_revenue]

    if country is not None:
        query += " AND UPPER(country) = UPPER(?)"
        parameters.append(country)

    row = connection.execute(
        query, parameters, 
        ).fetchone()
    connection.close()
    return {"total_revenue" : round(row["total_revenue"],2),
            "transaction_count": row["transaction_count"]}

def create_transaction(country:str, revenue:float):
    connection = get_connection()
    cursor = connection.execute(
        """INSERT INTO transactions(country, revenue)
        VALUES(?,?)""",
        (country.upper(), revenue),
    )
    connection.commit()

    transaction_id = cursor.lastrowid

    connection.close()
    return{
        "id": transaction_id,
        "country": country.upper(),
        "revenue": revenue,
    }