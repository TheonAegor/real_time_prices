PRICE_PRODUCER_PROJECT_PATH ?= price_producer
FRONTEND_PROJECT_PATH ?= frontend 
PROJECT_NAME ?= pricetransfer
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= real_time_prices
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

sdist: clean
	python3 setup.py sdist

clean:
	rm -fr *.egg-info dist

clean_all: clean
	cd $(PRICE_PRODUCER_PROJECT_PATH) && $(MAKE) clean
	cd $(FRONTEND_PROJECT_PATH) && $(MAKE) clean

build: sdist
	docker build -t $(PROJECT_NAME):$(VERSION) .

build_server: build
	cd $(PRICE_PRODUCER_PROJECT_PATH) && $(MAKE) build

build_front: 
	cd $(FRONTEND_PROJECT_PATH) && $(MAKE) build

build_all: docker_stop build
	cd $(PRICE_PRODUCER_PROJECT_PATH) && $(MAKE) build
	cd $(FRONTEND_PROJECT_PATH) && $(MAKE) build

docker_clean:
	DOCKER_DANGLING_IMAGES=$(docker images -f dangling=true -q);
	-docker rmi $(DOCKER_DANGLING_IMAGES)
	docker container prune --force

docker_stop: 
	docker-compose down
	make docker_clean

run_kafka: build_all
	docker-compose up zookeeper broker price-producer

run_transfer: build
	docker-compose up price-transfer

run_server: build_server
	docker-compose up zookeeper broker price-producer price-transfer

run_frontend: build_front
	docker-compose up frontend

run_all: build_all
	docker-compose up
# run_