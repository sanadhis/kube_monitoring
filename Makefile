all: build

DOCKER_REPO?=sanadhis/kube-monitoring
VERSION?=0.1

PWD:=$(shell pwd)

build:
	docker build -t $(DOCKER_REPO):$(VERSION) -f Dockerfile $(PWD)

push:
	docker push $(DOCKER_REPO):$(VERSION)