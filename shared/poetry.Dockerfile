FROM python:3.10-slim-bullseye
WORKDIR /opt/app
ONBUILD ARG REQUIREMENTS_TXT=requirements.txt
ONBUILD ARG SOURCE_DIR=.
ONBUILD COPY ${REQUIREMENTS_TXT} ./requirements.txt
ONBUILD RUN pip install -r requirements.txt
ONBUILD COPY ${SOURCE_DIR}/. .
