#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 NGROK_AUTHTOKEN GOOGLE_PROJECT_ID USERNAME PASSWORD" >&2
  exit 1
fi

rm -r server
cp -r ../../server/ .
docker container stop raspberrypi
docker container ls --all | grep raspberrypi | awk '{print $1}' | xargs docker container rm
docker image ls | grep raspberrypi | awk '{print $3}' | xargs docker image rm
docker build . --build-arg ngrok_auth_token=$1 --build-arg google_actions_project_id=$2 --build-arg user=$3 --build-arg password=$4 --tag=raspberrypi:v0.0.1
docker run -d --name raspberrypi -p 8080:65177 raspberrypi:v0.0.1
