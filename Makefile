.PHONY: up down test lint seed

up:
	cd deploy && docker compose up --build

down:
	cd deploy && docker compose down

test:
	cd backend && python -m pytest

lint:
	cd backend && ruff check . && ruff format --check .

seed:
	cd backend && python -m app.seed

.PHONY: migrate migrate-gen migrate-down

migrate-gen:
	cd backend && alembic revision --autogenerate -m "$(msg)"

migrate:
	cd backend && alembic upgrade head

migrate-down:
	cd backend && alembic downgrade -1