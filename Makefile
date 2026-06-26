.PHONY: up down test lint

up:
	cd deploy && docker compose up --build

down:
	cd deploy && docker compose down

test:
	cd backend && python -m pytest

lint:
	cd backend && ruff check . && ruff format --check .