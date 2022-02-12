DEV_FILE = dev.yml
PROD_FILE = prod.yml
QA_FILE = qa.yml
DEV_DOCKER_COMPOSE=docker-compose -f $(DEV_FILE)
PROD_DOCKER_COMPOSE=docker-compose -f $(PROD_FILE)
QA_DOCKER_COMPOSE=docker-compose -f $(QA_FILE)
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
qa-build:
	@echo "Now running in QA"
	@$(QA_DOCKER_COMPOSE) up --build
qa-clean: # Removes all orphans processes
	@echo "Cleaning up processes for docker-compose"
	@$(QA_DOCKER_COMPOSE) down -v
#===============================================#
#     Application specific commands #
#===============================================#
fetch:
	@echo "Fetching latest sub-modules!"
	git submodule update --init --recursive
generate-schema: # Runs generate schema command from go makefile
	$(MAKE) -C backend/go/src generate-schema
go-format: # Formats the go file
	$(MAKE) -C backend/go/src go-format
backend-format:
	@echo "formatting the backend!"
	@$(DEV_DOCKER_COMPOSE) exec pubsub-api-backend-v1 black src/
graphql-format:
	@echo "formatting grapqhl!"
	@$(DEV_DOCKER_COMPOSE) exec grapqhl go fmt .
frontend-format:
	@echo "formatting the frontend"
	@$(DEV_DOCKER_COMPOSE) exec pubsub-api-frontend prettier --write src/
format: # Formats all the files
	@echo "Formatting everything!"
	backend-format grapqhl-format frontend-format