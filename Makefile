.PHONY: help up down test lint gen-types dev-backend dev-frontend

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services
	cd deploy && docker compose up -d

down: ## Stop all services
	cd deploy && docker compose down

test: ## Run all tests
	cd services/ingestion && python -m pytest
	cd services/location && python -m pytest
	cd services/analytics && python -m pytest
	cd services/map && python -m pytest
	cd frontend && npm test

lint: ## Run linters
	cd services/ingestion && python -m ruff check .
	cd services/location && python -m ruff check .
	cd services/analytics && python -m ruff check .
	cd services/map && python -m ruff check .
	cd frontend && npm run lint

gen-types: ## Generate TypeScript types from OpenAPI specs
	./scripts/generate-types.sh

dev-backend: ## Run all backend services in dev mode (parallel)
	@cd services/ingestion && uvicorn src.main:app --reload --port 8000 & \
	cd services/location && uvicorn src.main:app --reload --port 8001 & \
	cd services/analytics && uvicorn src.main:app --reload --port 8002 & \
	cd services/map && uvicorn src.main:app --reload --port 8003 & \
	wait

dev-frontend: ## Run frontend in dev mode
	cd frontend && npm run dev

dev: dev-backend dev-frontend ## Run everything (use two terminals)