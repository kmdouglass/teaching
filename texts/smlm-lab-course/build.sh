#!/usr/bin/env sh

set -o errexit

SERVICE_NAME=build-manual

docker-compose run -u $(id -u):$(id -g) "$SERVICE_NAME"
