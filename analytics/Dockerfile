# Collect all the dependencies with poetry
FROM python:3.10-slim-bullseye as base
ENV POETRY_VERSION=1.1.12 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    APP_DIR="/opt/app" \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="${PYSETUP_PATH}/.venv"

# /// ****** BUILD PHASE ****** ///
# Minimal dependencies
FROM base as min-builder
RUN pip install poetry==${POETRY_VERSION} \
    && poetry config virtualenvs.create false

# Install the python requirements with poetry
# This is cached unless the dependencies change
WORKDIR ${PYSETUP_PATH}
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Install dev dependencies as well
FROM min-builder as dev-builder
WORKDIR ${PYSETUP_PATH}
RUN poetry install

# /// ****** TARGET PHASE ****** ///
FROM base as development
COPY --from=dev-builder ${PYSETUP_PATH} ${PYSETUP_PATH}
COPY --from=dev-builder ${POETRY_HOME} ${POETRY_HOME}

WORKDIR ${APP_DIR}
COPY . .
