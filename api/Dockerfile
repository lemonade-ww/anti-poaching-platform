FROM pig208/poetry:3.10-onbuild as production
WORKDIR /opt/app
CMD ["uvicorn", "--host", "0.0.0.0", "api.main:app"]

FROM pig208/poetry:3.10-onbuild as development
WORKDIR /opt/app
CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "api.main:app"]
