#!/bin/bash
# Railway startup script for Luna Noir Bot

# Set default port if not provided
export PORT=${PORT:-8080}

echo "Starting Luna Noir Bot on port $PORT"

# Start gunicorn with the PORT variable
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 src.server.app:app

