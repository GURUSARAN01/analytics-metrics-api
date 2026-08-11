import pytest

from app import database

@pytest.fixture(autouse=True)
def test_database(tmp_path, monkeypatch):
    test_db_path = tmp_path/"test_analytics.db"

    monkeypatch.setattr(database, "DATABASE_PATH", test_db_path)

    database.initialize_database()
    database.seed_database()

    yield