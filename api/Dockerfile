# syntax = edrevo/dockerfile-plus
INCLUDE+ shared/poetry.Dockerfile

FROM production-base as production
WORKDIR ${APP_DIR}
CMD uvicorn api.main:app

FROM development-base as development
WORKDIR ${APP_DIR}
CMD uvicorn api.main:app --reload
