#!/bin/bash

docker container stop raspberry-arm-prod
docker container ls --all | grep raspberry-arm-prod | awk '{print $1}' | xargs docker container rm
docker image ls | grep raspberry-arm-prod | awk '{print $3}' | xargs docker image rm
docker build . --tag=raspberry-arm-prod:v0.0.1
docker run -d --name raspberry-arm-prod raspberry-arm-prod:v0.0.1