# Use this dockerfile for different context
# Adapted from https://github.com/michaeloliverx/python-poetry-docker-example/blob/master/docker/Dockerfile

# Collect all the dependencies with poetry
FROM python:3.10-slim-bullseye as base
# Override SERVICE_ROOT when the build context is not where
# your pyproject.toml and poetry.lock located.
ARG SERVICE_ROOT=.
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
    SERVICE_ROOT="${SERVICE_ROOT}"
ENV VENV_PATH="${PYSETUP_PATH}/.venv" \
    PATH="${POETRY_HOME}/bin:${VENV_PATH}/bin:${PATH}"

# =================================
# ||| ****** BUILD PHASE ****** |||
# =================================
# Minimal dependencies
FROM base as min-builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# Install poetry with version POETRY_VERSION to POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -
# Install the python requirements with poetry
# This is cached unless the dependencies change
WORKDIR ${PYSETUP_PATH}
COPY ${SERVICE_ROOT}/pyproject.toml ${SERVICE_ROOT}/poetry.lock ./
RUN poetry install --no-dev

# Install dev dependencies as well
FROM min-builder as dev-builder
WORKDIR ${PYSETUP_PATH}
RUN poetry install

# ==================================
# ||| ****** TARGET PHASE ****** |||
# ==================================
FROM base as production-base
COPY --from=min-builder ${VENV_PATH} ${VENV_PATH}

WORKDIR ${APP_DIR}
COPY ${SERVICE_ROOT}/. .

FROM base as development-base
COPY --from=dev-builder ${PYSETUP_PATH} ${PYSETUP_PATH}
COPY --from=dev-builder ${POETRY_HOME} ${POETRY_HOME}

WORKDIR ${APP_DIR}
COPY ${SERVICE_ROOT}/. .
