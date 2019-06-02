#!/bin/bash

rm -r setup
cp -r ../../script/setup .
rm -r qemu-arm-static
cp /usr/bin/qemu-arm-static .
docker image ls | grep msh-arm | awk '{print $3}' | xargs docker image rm
docker build . --tag=msh-arm:v0.0.1