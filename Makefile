APP_NAME=astarcppdev:1.0
MKDIR_P = mkdir -p

HOST_UID ?= $(strip $(if $(shell id -u),$(shell id -u),4000))

build: ## Build the container
	cd docker; \
	docker build -t $(APP_NAME) .

run:
	${MKDIR_P} $(HOME)/.m2
	docker run --entrypoint /bin/bash -it --rm --network=host -u $(HOST_UID) -v $(HOME)/.m2:/home/builder/.m2 -v $(shell pwd):/maze $(APP_NAME)
