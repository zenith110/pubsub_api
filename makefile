DEV_FILE = docker-compose.yaml
PROD_FILE = docker-compose-prod.yaml
DEV_DOCKER_COMPOSE=docker-compose -f $(DEV_FILE)
PROD_DOCKER_COMPOSE=docker-compose -f $(PROD_FILE)
default: build

#==================================================#
# Builds and does other docker functionality #
#==================================================#
build: # Builds using all the dockerfiles and docker-compose provided
	@echo "Building pubsub-backend, and backend"
	@$(DEV_DOCKER_COMPOSE) up --build
clean: # Removes all orphans processes
	@echo "Cleaning up processes for docker-compose"
	@$(DEV_DOCKER_COMPOSE) down -v
detached: # Runs the containers in daemon mode
	@echo "Running processes in detached mode!"
	@$(DEV_DOCKER_COMPOSE) up -d --build
prod-build:
	@echo "Now running in prod enviroment"
	@$(PROD_DOCKER_COMPOSE) up --build
prod-detached:
	@echo "Now running in prod enviroment"
	@$(PROD_DOCKER_COMPOSE) up -d --build

#===============================================#
#     Application specific commands #
#===============================================#
fetch:
	@echo "Fetching latest sub-modules!"
	git submodule update --init --recursive