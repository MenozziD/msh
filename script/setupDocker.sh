#!/bin/bash

if [ "$#" -ne 5 ]; then
  echo "Usage: $0 GOOGLE_PROJECT_ID USERNAME PASSWORD DOMINIO_OAUTH DOMINIO_WEBAPP" >&2
  exit 1
fi

sudo apt-get remove docker docker-engine docker.io containerd runc -y
sudo apt-get update -y
sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
apt-cache madison docker-ce
sudo apt-get install docker-ce=5:18.09.1~3-0~debian-stretch docker-ce-cli=5:18.09.1~3-0~debian-stretch containerd.io -y
apt-get install qemu-user -y
cd ../Docker/base_image
sudo docker build . --tag=msh:v0.0.1
cp ../../server ../raspberry_image
cd ../raspberry_image
sudo docker build . --build-arg google_actions_project_id=$1 --build-arg user=$2 --build-arg password=$3 --build-arg dominio_oauth=$4 --build-arg dominio_webapp=$5 --tag=raspberrypi:v0.0.1
sudo docker run -d --name raspberrypi -p 8080:65177 raspberrypi:v0.0.1
