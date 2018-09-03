#!/bin/bash

# $1 - Version tag
# Use arm32v7 for arm images
# Use amd64 for 64bit

docker build -t egeldenhuys/dalla-stats-logger:$1 ./logger
docker push egeldenhuys/dalla-stats-logger:$1

docker build -t egeldenhuys/dalla-stats-ui:$1 ./web-server
docker push egeldenhuys/dalla-stats-ui:$1
