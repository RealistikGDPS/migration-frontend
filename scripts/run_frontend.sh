#!/bin/bash
set -euo pipefail

echo "Starting server..."
exec uvicorn migration_frontend.main:asgi_app \
    --host $HTTP_HOST \
    --port $HTTP_PORT \
    --reload
