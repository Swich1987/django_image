.PHONY: run lint test fmt migrations migrate help
.DEFAULT_GOAL := help

run:
	python manage.py runserver 0.0.0.0:8080

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

full_run:
	make migrate
	make run

help:
	@echo "run - Start the application"
	@echo "lint - Run linters to check code"
	@echo "fmt - Format and check code"
	@echo "test - Run all unit tests"
	@echo "migrations - Create new migrations for changes"
	@echo "migrate - Apply database migrations"
