# syntax = edrevo/dockerfile-plus
INCLUDE+ shared/poetry.Dockerfile

# Mount the source code in ${SOURCE_DIR}
# where you want to run the linter
FROM development-base as lint
ARG SOURCE_DIRNAME=.
ENV SOURCE_DIRNAME=${SOURCE_DIRNAME}
WORKDIR ${APP_DIR}
COPY ./shared/lint.sh /opt/tools/lint.sh
ENTRYPOINT [ "/opt/tools/lint.sh" ]
