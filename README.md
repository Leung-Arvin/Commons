# Commons

**Open-source indoor location and space utilization platform.**

---

Commons ingests real-time location signals and turns them into floor-plan
visualizations and space-utilization insights. It pairs a FastAPI + TimescaleDB
backend with a React map-based frontend.

## Tech Stack

| Layer        | Technology                                                        |
| ------------ | ----------------------------------------------------------------- |
| **Backend**  | FastAPI, SQLAlchemy (async), Alembic, Pydantic v2                  |
| **Frontend** | React 19, Vite, TypeScript, Tailwind CSS, Leaflet, Recharts       |
| **Data**     | TimescaleDB (PostgreSQL), Redis                                   |
| **Streaming**| Redpanda (Kafka API)                                               |

## Quick Start

The fastest way to run the full stack (backend, Postgres/TimescaleDB, Redis,
and Redpanda) is via Docker Compose:

```bash
make up
```

This builds and starts every service. The backend API will be available at
**http://localhost:8000** (docs at http://localhost:8000/docs).

To tear everything down:

```bash
make down
```

## Setup Guide

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Python](https://www.python.org/) 3.11+
- [Node.js](https://nodejs.org/) 20+ and npm

### 1. Backend

The backend lives in `backend/`. For local development outside Docker:

**macOS / Linux:**

```bash
cd backend

# Create a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[test,dev]"

# Start the database (Postgres/TimescaleDB on localhost:5433)
( cd ../deploy && docker compose up -d postgres )

# Run database migrations
alembic upgrade head

# Start the API with hot reload
uvicorn app.main:app --reload --port 8000
```

**Windows (PowerShell):**

```powershell
cd backend

# Create a virtual environment and install dependencies
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[test,dev]"

# Start the database (Postgres/TimescaleDB on localhost:5433)
cd ..\deploy; docker compose up -d postgres; cd ..\backend

# Run database migrations
alembic upgrade head

# Start the API with hot reload
uvicorn app.main:app --reload --port 8000
```

Configuration is read from environment variables (and an optional `.env` file)
using the `COMMONS_` prefix:

| Variable                 | Description                          | Default (Compose)                                          |
| ------------------------ | ------------------------------------ | ---------------------------------------------------------- |
| `COMMONS_DATABASE_URL`   | Async Postgres/TimescaleDB DSN       | `postgresql+asyncpg://user:pass@postgres:5432/commons`     |
| `COMMONS_REDIS_URL`      | Redis connection URL                 | `redis://redis:6379`                                       |
| `COMMONS_KAFKA_BROKER`   | Redpanda/Kafka broker address        | `redpanda:9092`                                            |

> When running outside Docker, point these at your local services — e.g.
> `postgres:5432` becomes `localhost:5433` (the port Compose publishes).

### 2. Frontend

The frontend lives in `frontend/` (Vite + React):

```bash
cd frontend
npm install
npm run dev
```

The dev server runs at **http://localhost:5173** and talks to the backend API.

### 3. Shared types

OpenAPI-derived TypeScript types are generated into `shared/`:

```bash
./scripts/generate-types.sh
```

## Common Tasks

All commands are available through the `Makefile` at the repo root:

| Command            | What it does                                            |
| ------------------ | ------------------------------------------------------- |
| `make up`          | Build and start the full stack via Docker Compose       |
| `make down`        | Stop and remove the stack                               |
| `make test`        | Run the backend test suite (`pytest`)                   |
| `make lint`        | Lint and format-check the backend (`ruff`)              |
| `make migrate`     | Apply migrations (`alembic upgrade head`)               |
| `make migrate-gen msg="..."` | Autogenerate a new migration revision        |
| `make migrate-down`| Roll back the last migration                            |

## Project Structure

```
.
├── backend/        # FastAPI service, SQLAlchemy models, Alembic migrations
├── frontend/       # React + Vite app (floor plans, map view)
├── deploy/         # docker-compose.yml for the full stack
├── shared/         # OpenAPI spec & generated TypeScript types
├── scripts/        # Tooling (type generation, etc.)
└── Makefile        # Common developer commands
```
