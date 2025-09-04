FROM python:3.12-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY alembic.ini .
COPY alembic ./alembic
COPY pytest.ini .
COPY Makefile .
COPY readme.md .

EXPOSE 8000
ENV UVICORN_HOST="0.0.0.0" \
    UVICORN_PORT="8000"

# Produção: sem --reload
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
