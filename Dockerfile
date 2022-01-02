FROM python:3.10-slim-bullseye
WORKDIR /app

# Install the python requirements
COPY requirements requirements
RUN apt update \
    && apt install -y gcc python3-dev libpq-dev \
    && pip install -r requirements/dev.txt
