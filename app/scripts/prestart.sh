#!/usr/bin/env bash

echo "Start migrations..."

alembic upgrade head

echo "Migrations is succesfully!"

exec "$@"