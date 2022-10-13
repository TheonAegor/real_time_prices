PROJECT_NAME ?= frontend
VERSION = 0.0.1
PROJECT_NAMESPACE ?= real_time_prices
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

clean:
	rm -rf ./build

build: clean
	npm install
	npm run build
	docker build -t $(PROJECT_NAME):$(VERSION) .

docker_run:
	docker run -d -p 8080:8080 $(PROJECT_NAME):$(VERSION)