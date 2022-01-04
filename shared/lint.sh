#!/bin/sh

set -e

TARGETS=$(find $1 -type f -name '*.py')

set -x

poetry run black $TARGETS
poetry run isort $TARGETS
poetry run mypy $TARGETS
