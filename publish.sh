#!/bin/bash

# $1 - Version tag

docker build -t egeldenhuys/dalla-stats-logger:$1 ./logger
docker tag egeldenhuys/dalla-stats-logger:$1 egeldenhuys/dalla-stats-logger:latest
docker push egeldenhuys/dalla-stats-logger:$1
docker push egeldenhuys/dalla-stats-logger:latest

docker build -t egeldenhuys/dalla-stats-ui:$1 ./web-server
docker tag egeldenhuys/dalla-stats-ui:$1 egeldenhuys/dalla-stats-ui:latest
docker push egeldenhuys/dalla-stats-ui:$1
docker push egeldenhuys/dalla-stats-ui:latest

docker build -t egeldenhuys/dalla-stats-db:$1 ./db
docker tag egeldenhuys/dalla-stats-db:$1 egeldenhuys/dalla-stats-db:latest
docker push egeldenhuys/dalla-stats-db:$1
docker push egeldenhuys/dalla-stats-db:latest

