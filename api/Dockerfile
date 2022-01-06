# syntax = edrevo/dockerfile-plus
INCLUDE+ shared/poetry.Dockerfile

FROM production-base as production
WORKDIR ${APP_DIR}
CMD uvicorn --host 0.0.0.0 api.main:app

FROM development-base as development
WORKDIR ${APP_DIR}
CMD uvicorn --reload --host 0.0.0.0 api.main:app
