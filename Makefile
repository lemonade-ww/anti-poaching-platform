# Arguments to use the overriden docker-compose file
PROD_COMPOSE_ARGS = -f docker-compose.yml \
		-f docker-compose.production.yml \

export DOCKER_BUILDKIT = 1
export COMPOSE_DOCKER_CLI_BUILD = 1

REVISION ?= 5ce2e23
THIS_FILE := $(lastword $(MAKEFILE_LIST))

help:
	@echo "make build - Build all dependencies"
	@echo "make push-latest - Push and update the docker registry"
	@echo "make run-dev - Run the dev build"
	@echo "make run-prod - Run the prod build"

build: build-prod build-dev

.PHONY: build-dev
build-dev: update-revision
	@echo "Building dev revision ${REVISION}"
	REVISION=${REVISION} docker compose \
		build --parallel

.PHONY: build-prod
build-prod: update-revision
	@echo "Building prod revision ${REVISION}"
	REVISION=${REVISION} docker compose $(PROD_COMPOSE_ARGS) \
		build --parallel

.PHONY: update-revision
update-revision:
	@set -e; \
		NEW_REVISION=$$(git rev-parse --short HEAD); \
		sed -i "0,/REVISION ?= */{s/REVISION ?= .*/REVISION ?= $${NEW_REVISION}/}" $(THIS_FILE); \
		test $${NEW_REVISION} = $(REVISION) && echo "revision unchanged" || echo "$(REVISION) => $${NEW_REVISION}"

.PHONY: push
push:
	@echo pushing $(REVISION)
	REVISION=$(REVISION) docker compose push
	REVISION=$(REVISION) docker compose \
		-f docker-compose.yml \
		-f docker-compose.production.yml \
		push

.PHONY: push-latest
push-latest:
	@$(MAKE) -f $(THIS_FILE) push
	@REVISION=latest $(MAKE) -f $(THIS_FILE) push

.PHONY: run-dev
run-dev:
	docker compose up -d

.PHONY: run-prod
run-prod:
	docker compose $(PROD_COMPOSE_ARGS) up -d
