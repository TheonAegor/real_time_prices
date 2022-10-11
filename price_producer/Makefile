PROJECT_NAME ?= priceproducer
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= real_time_prices
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)


clean:
	rm -fr *.egg-info dist

sdist: clean
	python3 setup.py sdist

docker2: sdist
	docker build  --target=api -t $(PROJECT_NAME):$(VERSION) .

build: sdist
	docker build  --target=api -t $(PROJECT_NAME):$(VERSION) .

docker: sdist
	docker-compose down
	docker container prune --force
	docker build --target=api -t $(PROJECT_NAME):$(VERSION) .