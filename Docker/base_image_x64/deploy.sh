#!/bin/bash

rm -r setup
cp -r ../../script/setup .
docker image ls | grep msh-x64 | awk '{print $3}' | xargs docker image rm
docker build . --tag=msh-x64:v0.0.1