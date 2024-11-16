#!/bin/sh

echo "starting ..."
echo "nslookup ..."
nslookup iis_database

env

set -e

echo "alembic upgrade ..."

poetry run alembic upgrade head

echo "api starting ..."

exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 1
