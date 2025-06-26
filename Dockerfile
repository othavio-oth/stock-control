FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY alembic.ini .
COPY alembic ./alembic
COPY pytest.ini .
COPY Makefile .
COPY readme.md .

EXPOSE 8000

ENV UVICORN_HOST="0.0.0.0"
ENV UVICORN_PORT="8000"

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]