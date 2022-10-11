PRICE_PRODUCER_PROJECT_PATH ?= price_producer
PROJECT_NAME ?= pricetransfer
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= real_time_prices
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

clean_all:
	cd $(PRICE_PRODUCER_PROJECT_PATH) && $(MAKE) clean

build_all:
	cd $(PRICE_PRODUCER_PROJECT_PATH) && $(MAKE) build
	docker build -t $(PROJECT_NAME):$(VERSION) .

clean:
	rm -fr *.egg-info dist

sdist: clean
	python3 setup.py sdist

build: sdist
	docker build  --target=transfer_api -t $(PROJECT_NAME):$(VERSION) .
	#docker build -t $(PROJECT_NAME):$(VERSION) .

run_kafka: build_all
	docker-compose down
	docker container prune --force
	docker-compose up zookeeper broker price-producer

run_transfer: build
	docker container prune --force
	docker-compose up price-transfer