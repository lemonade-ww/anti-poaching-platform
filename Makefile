# Arguments to use the overriden docker-compose file
PROD_COMPOSE_ARGS := -f docker-compose.yml \
		-f docker-compose.production.yml \

DEV_COMPOSE_ARGS := -f docker-compose.yml \
		-f docker-compose.development.yml \

LINT_COMPOSE_ARGS := -f docker-compose.lint.yml

SERVICES := api analytics

export DOCKER_BUILDKIT = 1
export COMPOSE_DOCKER_CLI_BUILD = 1

REVISION ?= 25af745
THIS_FILE := $(lastword $(MAKEFILE_LIST))
SECRETS_DIR := secrets
SECRET_NAMES := pg_password pg_user
DEV_SECRETS := $(addprefix $(SECRETS_DIR)/dev/,$(SECRET_NAMES))
PROD_SECRETS := $(addprefix $(SECRETS_DIR)/prod/,$(SECRET_NAMES))

help:
	@echo "make build - Build all dependencies"
	@echo "make push-latest - Push and update the docker registry"
	@echo "make run-dev - Run the dev build"
	@echo "make run-prod - Run the prod build"

build: build-prod build-dev

all-secrets: $(PROD_SECRETS) $(DEV_SECRETS)

$(SECRETS_DIR):
	mkdir -p secrets

$(SECRETS_DIR)/%: $(SECRETS_DIR)
	mkdir -p $@

$(DEV_SECRETS): $(SECRETS_DIR)/dev
	export TMP=$@; echo test$${TMP##*/} > $@

$(PROD_SECRETS): $(SECRETS_DIR)/prod
	export TMP=$@; echo test$${TMP##*/} > $@

.PHONY: build-dev
build-dev:
	@echo "Building dev revision ${REVISION}"
	REVISION=${REVISION} docker compose $(DEV_COMPOSE_ARGS) \
		build $(SERVICES) --parallel

.PHONY: build-prod
build-prod:
	@echo "Building prod revision ${REVISION}"
	REVISION=${REVISION} docker compose $(PROD_COMPOSE_ARGS) \
		build $(SERVICES) --parallel

.PHONY: build-lint
build-lint:
	REVISION=${REVISION} docker compose $(LINT_COMPOSE_ARGS) \
		build $(SERVICES) --parallel

.PHONY: update-revision
update-revision:
	@set -e; \
		NEW_REVISION=$$(git rev-parse --short HEAD); \
		sed -i "0,/REVISION ?= */{s/REVISION ?= .*/REVISION ?= $${NEW_REVISION}/}" $(THIS_FILE); \
		test $${NEW_REVISION} = $(REVISION) && echo "revision unchanged" || echo "$(REVISION) => $${NEW_REVISION}"

.PHONY: push
push:
	@echo pushing $(REVISION)
	REVISION=$(REVISION) docker compose $(DEV_COMPOSE_ARGS) push $(SERVICES)
	REVISION=$(REVISION) docker compose $(PROD_COMPOSE_ARGS) push $(SERVICES)

.PHONY: push-latest
push-latest:
	@$(MAKE) -f $(THIS_FILE) update-revision

	@$(MAKE) -f $(THIS_FILE) build
	@REVISION=latest $(MAKE) -f $(THIS_FILE) build
	@$(MAKE) -f $(THIS_FILE) push
	@REVISION=latest $(MAKE) -f $(THIS_FILE) push

.PHONY: bump-image
bump-image: push-latest
	git add $(THIS_FILE)
	git commit -m "docker: Bump image revision"

.PHONY: run-dev
run-dev: $(DEV_SECRETS)
	REVISION=$(REVISION) docker compose $(DEV_COMPOSE_ARGS) up -d --force-recreate $(SERVICES)

.PHONY: run-prod
run-prod: $(PROD_SECRETS)
	REVISION=$(REVISION) docker compose $(PROD_COMPOSE_ARGS) up -d $(SERVICES)

.PHONY: run-lint
run-lint:
	REVISION=$(REVISION) docker compose $(LINT_COMPOSE_ARGS) up

.PHONY: clean-containers
clean-containers:
	docker compose $(DEV_COMPOSE_ARGS) rm
	docker compose $(PROD_COMPOSE_ARGS) rm
	docker compose $(LINT_COMPOSE_ARGS) rm

.PHONY: clean-db
clean-db:
	docker compose down db
	docker volume rm anti-poaching-platform_pgdata
