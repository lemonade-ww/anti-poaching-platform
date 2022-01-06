#!/bin/sh

set -e

TARGETS=$(find ${APP_DIR}/${SOURCE_DIRNAME} -type f -name '*.py')

set -x

poetry run black $TARGETS
poetry run isort $TARGETS
poetry run mypy $TARGETS
