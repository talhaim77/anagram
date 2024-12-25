#!/bin/sh

echo "Running Alembic migrations..."
alembic upgrade head

# Execute the CMD from the Dockerfile
exec "$@"