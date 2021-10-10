VENV_DIR := .venv
PYTHON_VENV := $(VENV_DIR)/bin/python
TARGETS := analytics server manage.py

.venv:
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements/dev.txt

clean:
	rm -rf .venv

.PHONY: requirements
requirements: .venv
	pip-compile --allow-unsafe --quiet requirements/common.in
	pip-compile --allow-unsafe --quiet requirements/dev.in

lint: .venv
	dir
	$(PYTHON_VENV) -m black $(TARGETS)
	$(PYTHON_VENV) -m isort $(TARGETS)
	$(PYTHON_VENV) -m mypy $(TARGETS)