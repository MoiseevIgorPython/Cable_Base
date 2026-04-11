#!/usr/bin/env bash

set -a
source .env.production
set +a

echo "Add Enum Types..."
PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${POSTGRES_HOST_DOCKER}" -U "${POSTGRES_USER}" -d "${POSTGRES_NAME}" -c "CREATE TYPE userrole AS ENUM ('ADMIN', 'USER')" 2>/dev/null || true
PGPASSWORD="${POSTGRES_PASSWORD}" psql -h "${POSTGRES_HOST_DOCKER}" -U "${POSTGRES_USER}" -d "${POSTGRES_NAME}" -c "CREATE TYPE department AS ENUM ('CABLE', 'TWIST')" 2>/dev/null || true
echo "Add Enum Types is succesfully!"

echo "Start migrations..."
alembic upgrade head
echo "Migrations is succesfully!"

echo "Add data in tables..."
python scripts/add_test_data.py
echo "Add data is succesfully!..."

exec "$@"
