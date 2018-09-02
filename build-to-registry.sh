#!/bin/bash

# Build images and deploy to local registry

docker build -t 127.0.0.1:5000/dalla-stats-logger:local ./logger
docker push 127.0.0.1:5000/dalla-stats-logger:local

docker build -t 127.0.0.1:5000/dalla-stats-ui:local ./web-server
docker push 127.0.0.1:5000/dalla-stats-ui:local

docker build -t 127.0.0.1:5000/dalla-stats-db:local ./db
docker push 127.0.0.1:5000/dalla-stats-db:local
