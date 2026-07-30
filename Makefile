.PHONY: help build up down logs test lint format

help:
	@echo "Commands: build, up, down, logs, test, lint, format"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	pytest -q

lint:
	ruff check . && black --check .

format:
	black . && ruff format .
