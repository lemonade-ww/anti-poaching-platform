#!/bin/sh

set -e

set -x

TARGETS=$(find $1 -type f -name '*.py')
exit 0
poetry run python -m black $TARGETS
poetry run python -m isort $TARGETS
poetry run python -m mypy $TARGETS
