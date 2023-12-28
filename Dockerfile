# Start from the official Python 3.11 image.
# Can be changed to any other Python 3.x image without changing the rest of the Dockerfile
ARG DOCKER_PYTHON_IMAGE="python:3.11"
FROM ${DOCKER_PYTHON_IMAGE} as base

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc (useful for production)
# PYTHONUNBUFFERED: Ensures our console output looks familiar and is not buffered by Docker, which is useful for logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

WORKDIR ${APP_HOME}

# Install libpq5 for PostgreSQL support. Using just runtime libraries to minimize image size
RUN apt-get update && apt-get install -y \
    libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ${APP_HOME}

# Create a non-root user "appuser" for running the application
# It's a best practice to not run applications as the root user for security reasons
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser ${APP_HOME}
USER appuser

# Expose port 8080 for the application. Adjust if your want to use a different port
ARG APP_PORT=8080
ENV APP_PORT=${APP_PORT}

EXPOSE ${APP_PORT}

CMD ["./docker-entrypoint.sh", "run"]
