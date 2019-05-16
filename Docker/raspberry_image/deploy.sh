#!/bin/bash

rm -r msh
cp -r ../../msh .
docker container stop raspberrypi
docker container ls --all | grep raspberrypi | awk '{print $1}' | xargs docker container rm
docker image ls | grep raspberrypi | awk '{print $3}' | xargs docker image rm
docker build . --tag=raspberrypi:v0.0.1
docker run -d --name raspberrypi -p 8080:65177 raspberrypi:v0.0.1
