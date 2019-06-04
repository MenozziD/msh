#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 NOME_WIFI PASSWORD_WIFI" >&2
  exit 1
fi

rm -r setup
cp -r ../../script/setup .
rm -r qemu-arm-static
cp /usr/bin/qemu-arm-static .
docker image ls | grep msh-arm | awk '{print $3}' | xargs docker image rm
docker build . --build-arg nome_wifi=$1 --build-arg password_wifi=$2 --tag=msh-arm:v0.0.1