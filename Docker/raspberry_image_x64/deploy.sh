#!/bin/bash

if [ "$#" -ne 5 ]; then
  echo "Usage: $0 GOOGLE_PROJECT_ID USERNAME PASSWORD DOMINIO_OAUTH DOMINIO_WEBAPP" >&2
  exit 1
fi

rm -r server
cp -r ../../server/ .
docker container stop raspberry-x64
docker container ls --all | grep raspberry-x64 | awk '{print $1}' | xargs docker container rm
docker image ls | grep raspberry-x64 | awk '{print $3}' | xargs docker image rm
docker build . --build-arg google_actions_project_id=$1 --build-arg user=$2 --build-arg password=$3 --build-arg dominio_oauth=$4 --build-arg dominio_webapp=$5 --tag=raspberry-x64:v0.0.1
docker run -d --name raspberry-x64 raspberry-x64:v0.0.1
