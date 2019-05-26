#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 NGROK_AUTHTOKEN GOOGLE_PROJECT_ID" >&2
  exit 1
fi

cd ../Docker/base_image
docker build . --tag=msh:v0.0.1
cp ../../msh ../raspberry_image
cd ../raspberry_image
docker build . --build-arg ngrok_auth_token=$1 --build-arg google_actions_project_id=$2 --tag=raspberrypi:v0.0.1
docker run -d --name raspberrypi -p 8080:65177 raspberrypi:v0.0.1
