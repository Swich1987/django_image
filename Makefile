.PHONY: run lint test fmt migrations migrate help
.DEFAULT_GOAL := help

run:
	python -m app

lint:
	isort . -c
	black . --check
	flake8 .
	mypy .

fmt:
	isort .
	black .
	flake8 .
	mypy .

test:
	pytest

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

help:
	@echo "run - Start the application"
	@echo "lint - Run linters to check code"
	@echo "fmt - Format and check code"
	@echo "test - Run all unit tests"
	@echo "migrations - Create new migrations for changes"
	@echo "migrate - Apply database migrations"
