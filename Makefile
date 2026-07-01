.PHONY: build test lint infra services run

build:
	docker-compose -f deploy/docker-compose/docker-compose.dev.yml build

test:
	cd packages/compliance-sdk && poetry run pytest
	for svc in services/*/; do cd $$svc && poetry run pytest && cd -; done

lint:
	ruff check .

infra:
	docker-compose -f deploy/docker-compose/docker-compose.infra.yml up -d

services:
	docker-compose -f deploy/docker-compose/docker-compose.services.yml up -d

run: infra services
.PHONY: run-obs
run-obs:
docker-compose -f deploy/docker-compose/docker-compose.observability.yml up -d
