#!/bin/bash

# $1 - Version tag

docker build -t egeldenhuys/dalla-stats-logger:$1 ./logger
docker push egeldenhuys/dalla-stats-logger

docker build -t egeldenhuys/dalla-stats-ui:$1 ./db
docker push egeldenhuys/dalla-stats-ui

docker build -t egeldenhuys/dalla-stats-db:$1 ./web-server
docker push egeldenhuys/dalla-stats-db

