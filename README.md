# Analytics Metrics API

## What it does
FastAPI analytics backend for transaction metrics.

## Features
- Revenue metrics with filters
- Transaction lookup
- Transaction creation
- Pydantic validation
- SQLite persistence
- Automated pytest coverage
- Docker containerization
- Persistent Docker volume

## Tech Stack
Python
FastAPI
Pydantic
SQLite
pytest
Docker

## Architecture
Client
  ↓
FastAPI routes
  ↓
Service layer
  ↓
SQLite database

## Run locally
pip install -r requirements.txt
python -m app.database
fastapi dev app/main.py

## Run tests
python -m pytest -v

## Run with Docker
docker build -t analytics-metrics-api .

docker volume create analytics-data

docker run --name analytics-api -p 127.0.0.1:8000:8000 -v analytics-data:/code/data analytics-metrics-api