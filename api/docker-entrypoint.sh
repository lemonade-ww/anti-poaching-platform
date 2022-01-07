#!/bin/sh

set -e

alembic upgrade head

if [ -z $PRODUCTION ];
then
    echo "Starting up in development"
    exec uvicorn --reload --host 0.0.0.0 api.main:app
else
    echo "Starting up in production"
    exec uvicorn --host 0.0.0.0 api.main:app
fi
