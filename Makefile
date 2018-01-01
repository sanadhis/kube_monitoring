all: build push

IMAGE_NAME?=sanadhis/kube-monitoring
VERSION?=0.1

PWD:=$(shell pwd)

build:
	docker build -t $(IMAGE_NAME):$(VERSION) -f Dockerfile $(PWD)

push:
	docker push $(IMAGE_NAME):$(VERSION)