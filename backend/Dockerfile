# Backend multi-stage build (Python 3.11) with Poetry
FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential curl git && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml poetry.lock* /app/
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction
COPY . /app

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
