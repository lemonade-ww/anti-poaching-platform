#!/bin/sh

set -e

TARGETS=$(find ${TARGET_DIR:-.} -type f -name '*.py')

black --target-version py310 $TARGETS
isort $TARGETS
mypy $TARGETS
