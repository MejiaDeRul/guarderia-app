# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
PIP_NO_CACHE_DIR=1 \
UVICORN_PORT=8000


WORKDIR /app


# System deps (only minimal since psycopg2-binary is used)
RUN apt-get update && apt-get install -y --no-install-recommends \
ca-certificates curl \
&& rm -rf /var/lib/apt/lists/*


# Install python deps first (better layer caching)
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt


# Copy app source
COPY app ./app


# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser


EXPOSE 8000


# Default command (can be overridden by compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]