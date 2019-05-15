IMAGE_VERSION=0.1
IMAGE_TAG:=$(REGISTRY_URL)/eks-traefik-notify

all: image push

.PHONY: clean
clean:
	echo 'clean'

.PHONY: image
image: 
	docker build -t $(IMAGE_TAG):$(IMAGE_VERSION) .

.PHONY: build
build:

.PHONY: push
push:
	docker push $(IMAGE_TAG):$(IMAGE_VERSION)

.PHONY: latest
latest:
	docker tag $(IMAGE_TAG):$(IMAGE_VERSION) $(IMAGE_TAG):latest
	docker push $(IMAGE_TAG):latest
	
	
