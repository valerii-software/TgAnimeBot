FROM python:3.13.0a3-slim

WORKDIR /app

COPY . /app/

RUN pip install poetry && poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root
