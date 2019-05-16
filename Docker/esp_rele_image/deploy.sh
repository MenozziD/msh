#!/bin/bash

docker container stop esprele
docker container ls --all | grep esprele | awk '{print $1}' | xargs docker container rm
docker image ls | grep esprele | awk '{print $3}' | xargs docker image rm
docker build . --tag=esprele:v0.0.1
docker run -d --name esprele -p 8081:8080 esprele:v0.0.1