FROM python:3.12-alpine

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

ENV \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.5.1

EXPOSE 8000

WORKDIR /fit_iis

RUN apk add --no-cache \
    gcc \
    libpq-dev \
    musl-dev \
    postgresql-dev

# Poetry Setup
COPY poetry.lock pyproject.toml ./
RUN pip install "poetry==$POETRY_VERSION" && \
    poetry export --output requirements.txt && \
    pip install --no-deps -r requirements.txt

COPY app app
COPY main.py main.py
COPY alembic alembic
COPY alembic.ini alembic.ini
COPY .entrypoint.sh .entrypoint.sh
