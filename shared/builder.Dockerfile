FROM python:3.10-bullseye
WORKDIR /opt/client
RUN pip install build twine
CMD ["python", "-m", "build"]
