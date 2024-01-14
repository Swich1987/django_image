#!/usr/bin/env sh

case "${1}" in
    "run")
        shift
        echo "Starting application, node $(hostname)..."
        exec make run
        ;;
    "full_run")
        shift
        echo "Starting application, node $(hostname)..."
        /app/wait-for-it.sh database:5432 -- make full_run
        ;;
    "lint")
        shift
        isort . -c
        black . --check
        flake8 .
        mypy .
        ;;
    "fmt")
        shift
        isort .
        black .
        flake8 .
        mypy .
        ;;
    "test")
        shift
        echo "Running tests..."
        exec pytest "${@}"
        ;;
    "migrations")
        shift
        echo "Creating migrations..."
        exec python manage.py makemigrations
        ;;
    "migrate")
        shift
        echo "Applying database migrations..."
        exec python manage.py migrate
        ;;
    "help")
        echo "Available commands: run lint fmt test migrations migrate help"
        ;;
    *)
        exec "${@}"
        ;;
esac
