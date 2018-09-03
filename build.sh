#!/bin/bash

# $1 - Version tag

docker build -t egeldenhuys/dalla-stats-logger:$1 ./logger
docker build -t egeldenhuys/dalla-stats-ui:$1 ./web-server
