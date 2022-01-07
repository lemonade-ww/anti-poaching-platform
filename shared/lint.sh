#!/bin/sh

set -e

TARGETS=$(find ${TARGET_DIR:-.} -type f -name '*.py')

black $TARGETS
isort $TARGETS
mypy $TARGETS
