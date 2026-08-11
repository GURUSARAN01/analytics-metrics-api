import sqlite3
from pathlib import Path

DATABASE_PATH = Path("data/analytics.db")

DATABASE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    connection = get_connection()

    connection.execute(
        """CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY,
        country TEXT NOT NULL,
        revenue REAL NOT NULL
        )"""
    )

    connection.commit()
    connection.close()

def seed_database():
    connection = get_connection()

    seed_transactions = [        
        (1, "DE", 120.50),
        (2, "DE", 89.99),
        (3, "FR", 75.00),
        (4, "UK", 220.00),
        (5, "FR", 130.25),]
    connection.executemany(
        """INSERT OR IGNORE INTO transactions(id, country, revenue)
        VALUES(?,?,?)""", seed_transactions,
    )
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()
    seed_database()