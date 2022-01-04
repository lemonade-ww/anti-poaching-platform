#!/bin/sh

set -e

TARGETS=$(find $1/ -type f -name '*.py')

set -x

poetry run python -m black $TARGETS
poetry run python -m isort $TARGETS
poetry run python -m mypy $TARGETS
