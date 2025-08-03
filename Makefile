dev:
	flask run --debug --port=8000

start:
	flask run

create-migration:
	alembic revision --autogenerate

migrate:
	alembic upgrade head
