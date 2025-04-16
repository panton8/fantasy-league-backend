DOCKER_COMPOSE_FILE = docker-compose.yml
APP_CONTAINER = web
PROJECT_DIR = /opt/fantasy_league/

build:
	docker-compose -f ${DOCKER_COMPOSE_FILE} build

up:
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d

stop:
	docker-compose -f ${DOCKER_COMPOSE_FILE} stop

down:
	docker-compose -f ${DOCKER_COMPOSE_FILE} down

migrate:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm web ./manage.py migrate --noinput

migrations:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm web ./manage.py makemigrations

pytest:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm -w ${PROJECT_DIR} -e HUEY_IMMEDIATE=True web pytest --cov-config=.coveragerc --cov=src -x --reuse-db src

dpytest:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm -w ${PROJECT_DIR} -e HUEY_IMMEDIATE=True web pytest -x --reuse-db --disable-warnings src

dpytest_reset:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm -w ${PROJECT_DIR} -e HUEY_IMMEDIATE=True web pytest -x src

fast_pytest:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm -w ${PROJECT_DIR} -e HUEY_IMMEDIATE=True web pytest -x --reuse-db --disable-warnings src -m "not slow"

collectstatic:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm  web ./manage.py collectstatic
logs:
	docker-compose -f ${DOCKER_COMPOSE_FILE} logs

rest_schema:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm  web ./manage.py spectacular --file rest_schema/schema.yml &> /dev/null
