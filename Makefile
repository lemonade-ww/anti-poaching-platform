# Arguments to use the overriden docker-compose file
PROD_COMPOSE_ARGS = -f docker-compose.yml \
		-f docker-compose.production.yml \

build: build-prod build-dev

push:
	docker compose push
	docker compose \
		-f docker-compose.yml \
		-f docker-compose.production.yml \
		push

build-dev:
	docker compose \
		build --parallel

build-prod:
	docker compose $(PROD_COMPOSE_ARGS) \
		build --parallel

run-dev:
	docker compose up -d

run-prod:
	docker compose $(PROD_COMPOSE_ARGS) up -d
