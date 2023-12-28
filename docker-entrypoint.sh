#!/usr/bin/env sh

case "${1}" in
    "run")
        shift
        echo "Starting application, node $(hostname)..."
        exec gunicorn myproject.wsgi:application --bind 0.0.0.0:${APP_PORT}
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
