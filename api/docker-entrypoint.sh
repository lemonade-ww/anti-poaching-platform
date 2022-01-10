#!/bin/sh

set -e

alembic upgrade head

if [ "$ENVIRONMENT" = development ];
then
    echo "Starting up in development"
    exec uvicorn --reload --host 0.0.0.0 api.main:app
else
    echo "Starting up in production"
    exec uvicorn --host 0.0.0.0 api.main:app
fi
