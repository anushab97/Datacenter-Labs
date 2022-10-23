#!/bin/sh
kubectl -n sentiment apply -f redis/redis-deployment.yaml
kubectl -n sentiment apply -f redis/redis-service.yaml
kubectl -n sentiment apply -f rabbitmq/rabbitmq-deployment.yaml
kubectl -n sentiment apply -f rabbitmq/rabbitmq-service.yaml
sleep 10s

kubectl -n sentiment apply -f rest/rest-deployment.yaml
kubectl -n sentiment apply -f rest/rest-service.yaml

kubectl -n sentiment apply -f logs/logs-deployment.yaml

kubectl -n sentiment apply -f worker/worker-deployment.yaml

