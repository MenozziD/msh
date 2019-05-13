#!/bin/bash

rm -r msh
cp -r ../../msh .
docker container stop raspberrypi
docker container ls --all | awk '{print $1}' | xargs docker container rm
docker build . --tag=msrheal:v0.0.1
docker run -d --name raspberrypi -p 8080:65177 msrheal:v0.0.1