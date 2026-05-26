# OpenTelemetry FastAPI Observability Project

This project is a learning-focused observability setup using FastAPI and OpenTelemetry (OTEL).

## Features

- FastAPI backend
- OpenTelemetry tracing
- Jaeger trace visualization
- PostgreSQL database instrumentation
- In-memory cache instrumentation
- Manual and automatic spans
- Multiple API endpoints
- Traffic generation script

## Tech Stack

- FastAPI
- OpenTelemetry
- Jaeger
- PostgreSQL
- Docker
- Python

## Endpoints

### GET /users
Fetches users from cache or PostgreSQL.

### POST /users
Adds a new user into PostgreSQL and clears cache.

### GET /products
Returns product list.

### GET /health
Health check endpoint.

## Observability Features

This project demonstrates:

- traces
- spans
- manual instrumentation
- automatic instrumentation
- cache hit/miss tracing
- database query tracing
- distributed tracing concepts

## Running The Project

### Start PostgreSQL

```bash
docker start postgres-db
```

### Start Jaeger

```bash
docker start jaeger
```

### Run FastAPI

```bash
python -m uvicorn main:app --reload
```

## Jaeger UI

```text
http://localhost:16686
```

## Swagger Docs

```text
http://127.0.0.1:8000/docs
```