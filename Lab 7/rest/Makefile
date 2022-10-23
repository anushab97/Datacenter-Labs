VERSION=v2
DOCKERUSER=anushab97

build:
	docker build -t sentiment-rest .

push:
	docker tag sentiment-rest anushab97/sentiment-rest:v2
	docker push anushab97/sentiment-rest:v2
	docker tag sentiment-rest $(DOCKERUSER)/sentiment-rest:latest
	docker push $(DOCKERUSER)/sentiment-rest:latest
