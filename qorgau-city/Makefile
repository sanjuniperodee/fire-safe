.DEFAULT_GOAL := help

# Executables (local)
DOCKER_COMP = docker-compose

CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

PRIVILEGES = ${APP} chown -R $(CURRENT_UID):$(CURRENT_GID)

# Executables
DOCKER_EXEC = $(DOCKER_COMP) exec

# Executables docker containers
APP = $(DOCKER_EXEC) app_backend

help: ## Help message
	@echo "Please choose a task:"
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m##/[33m/'

PROJECT_DIR=$(shell dirname $(realpath $(MAKEFILE_LIST)))

ifeq (manage,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

# Define the folders you want to scan (For windows use \, for unix system/docker use /)
# FOLDERS = .\src\auths\migrations .\src\objects\migrations .\src\providers\migrations
FOLDERS = ./src/auths/migrations ./src/objects/migrations ./src/providers/migrations

prod: build

install: build start migrate ## Spin-up the project with minimal data

build: ## Build docker containers
	$(DOCKER_COMP) build
	@echo ">>> Base build done!"

shell: ## Run bash inside superapp container
	${APP} bash

django_shell: ## Enter Django shell inside app_backend container
	${APP} python manage.py shell

rebuild: ## Build docker containers without cache
	$(DOCKER_COMP) build --no-cache
	@echo ">>> Rebuild done!"

start: ## Start all services
	${DOCKER_COMP} up -d
	@echo ">>> Containers started!"

cronjobs: ## Start cron_jobs
	${APP} python manage.py schedule_complaints_status_update
	@echo ">>> Cron jobs are created!"

stop: ## Stop all services
	${DOCKER_COMP} stop
	@echo ">>> Containers stopped!"

backup: ## Create backups of database
	@python src/backup/manage_backups.py backup $(FOLDERS)

restore: ## Restore backups
	@python src/backup/manage_backups.py restore $(FOLDERS)

destroy: ## Stop and remove all containers, networks, images, and volumes
	${DOCKER_COMP} down --volumes --remove-orphans
	@echo ">>> Containers destroyed!"

collectstatic: ## Collectstatic
	${APP} python manage.py collectstatic --noinput
	${APP} chown -R $(CURRENT_UID):$(CURRENT_GID) static
	@echo ">>> Controller done!"

makemigrations: ## Make migrations
	${APP} python manage.py makemigrations
	@echo ">>> Controller done!"

migrate: ## Create new migration
	${APP} python manage.py migrate
	@echo ">>> Migration done!"

runinit: ## Create documents and info
	${APP} python manage.py create_documents
	${APP} python manage.py import_json
	${APP} python manage.py create_subbuilding_parameters
	@echo ">>> Command done!"

test: ## Test applications
	${APP} python manage.py test test.test
	@echo ">>> Command done!"