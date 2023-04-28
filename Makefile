#REPO_NAME ?= "superdews_docker"
#REGION ?= "eu-central-1"
#PORTS ?= "80:80"
DOCKER_PLATFORM ?= --platform=linux/amd64

make_migrations:
	@docker-compose -f ./local.yml run --rm django python manage.py makemigrations

migrate:
	@docker-compose -f ./local.yml run --rm django python manage.py migrate

mm:make_migrations migrate

superuser:
	@docker-compose -f ./local.yml run --rm django python manage.py createsuperuser

collectstatic:
	@docker-compose -f ./local.yml run --rm django python manage.py collectstatic --no-input

exportdata:
	@docker-compose -f ./local.yml run --rm django python manage.py dumpdata --exclude=auth --exclude=contenttypes \
	--exclude=sessions --exclude=admin --exclude=django_celery_beat > data.json

importdata:
	@docker-compose -f ./local.yml run --rm django python manage.py loaddata data.json

update_dep:
	pip install pip-tools
	pip-compile --resolver=backtracking requirements/local.in
	pip-compile --resolver=backtracking requirements/production.in

enter_running:
	@docker-compose -f ./local.yml run --rm django sh

shell_plus:
	@docker-compose -f ./local.yml run --rm django python manage.py shell_plus --ipython

reset_db:
	@docker-compose -f ./local.yml run --rm django python manage.py reset_db --noinput

down_db:
	@docker-compose -f ./local.yml stop postgres

init_all: down_db reset_db mm

build:
	@docker-compose -f ./local.yml build

build_all: build collectstatic init_all

docker_clean:
	@docker system prune -a --volumes

#
#login_ecr:
#	@aws ecr get-login-password --region $(REGION) || docker login --username AWS --password-stdin $(ACCOUNT_ID).dkr.ecr.$(REGION).amazonaws.com
#
#login_public:
#	@aws ecr-public get-login-password --region us-east-1 || docker login --username AWS --password-stdin public.ecr.aws
