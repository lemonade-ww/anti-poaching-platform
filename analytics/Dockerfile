# syntax = edrevo/dockerfile-plus
INCLUDE+ shared/poetry.Dockerfile

FROM production-base as production

FROM development-base as development

FROM development as lint
WORKDIR ${APP_DIR}
COPY ./shared/lint.sh /opt/tools/lint.sh
CMD /opt/tools/lint.sh ${APP_DIR}/analytics
