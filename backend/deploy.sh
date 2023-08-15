#!/usr/bin/env bash

mkdir -p shared/nginx

docker-compose -f docker-compose.yml -f docker-compose-prod.yml up --build --remove-orphans -d

docker image prune -f
docker container prune -f
docker volume prune -f
docker network prune -f

