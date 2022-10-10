PROJECT_NAME ?= priceproducer
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= real_time_prices
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)


clean_all:
	rm -fr *.egg-info dist
	rm -fr price_producer/*.egg-info dist

sdist: clean_all
	python3 setup.py sdist
	python3 setup.py price_producer/sdist

docker2: sdist
	docker build  --target=api -t $(PROJECT_NAME):$(VERSION) .

docker: sdist
	docker-compose down
	docker container prune --force
	docker build --target=api -t $(PROJECT_NAME):$(VERSION) price_producer/.
	docker-compose up