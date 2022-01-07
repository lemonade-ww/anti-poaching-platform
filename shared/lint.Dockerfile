# Mount the source code in ${SOURCE_DIR}
# where you want to run the linter
FROM pig208/poetry:3.10-onbuild
WORKDIR /opt/app
COPY ./shared/lint.sh /opt/tools/lint.sh
ENTRYPOINT [ "/opt/tools/lint.sh" ]
