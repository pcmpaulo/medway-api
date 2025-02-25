create-virtualenv:
	pyenv install 3.11.10
	pyenv virtualenv 3.11.10 medway-api-3.11.10

activate-virtualenv:
	pyenv local medway-api-3.11.10

install-dependencies:
	pip install -r "./requirements.txt"

run-dev:
	 ENVIRONMENT=.env python app/manage.py runserver

run-prod:
	docker compose up --build

access-docker-bash:
	docker exec -it medway-api bash

start-database:
	docker compose up --detach db

stop-database:
	docker compose stop db

generate-migrations:
	python app/manage.py makemigrations

apply-migrations:
	ENVIRONMENT=.env python app/manage.py migrate

test:
	pytest --cov . --cov-config=.coveragerc --cov-report term-missing
