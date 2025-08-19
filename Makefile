include .env

migration_gen:
	cd src
	uv run alembic revision --autogenerate -m "makefile-generated migration"

migration_run:
	cd src
	uv run alembic upgrade head

web:
	uv run uvicorn app:app --reload

docker-up:
	docker compose -f docker-compose.yaml up -d

docker-rebuild:
	docker compose -f docker-compose.yaml up -d --build

docker-down:
	docker compose -f docker-compose.yaml down

docker-upgrade:
	make docker-down
	git fetch
	git pull origin
	make docker-rebuild