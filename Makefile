# test (restaurant site + reservations): run `make help`.
.DEFAULT_GOAL := help
.PHONY: help install run list test lint fmt check

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies (uv)
	uv sync

run: ## Serve the site and the booking endpoint on http://127.0.0.1:8000
	uv run reservations serve

list: ## Print upcoming reservations
	uv run reservations list

test: ## Run the tests
	uv run pytest -q

lint: ## ruff lint + format check
	uv run ruff check .
	uv run ruff format --check .

fmt: ## Format and fix what ruff can
	uv run ruff format .
	uv run ruff check --fix .

check: lint test ## Everything that must pass before a PR
