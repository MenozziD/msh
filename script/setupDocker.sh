#!/bin/bash

if [ "$#" -ne 5 ]; then
  echo "Usage: $0 GOOGLE_PROJECT_ID USERNAME PASSWORD DOMINIO_OAUTH DOMINIO_WEBAPP" >&2
  exit 1
fi

# INSTALLO DOCKER
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
sudo service docker start
# IMPOSTO DOCKER PER PARTIRE AL REBOOT
sudo update-rc.d docker enable
# INSTALLO QEMU
apt-get install qemu-user -y
# CREO IMMAGINE BASE ARM CON QEMU
cd ../Docker/base_image_ARM
sudo docker build . --tag=msh-arm:v0.0.1
# CREO IMMAGINE BASE ARM SENZA QEMU
cd ../Docker/base_image_ARM_prod
sudo docker build . --tag=msh-arm-prod:v0.0.1
# CREO IMMAGINE BASE X64
cd ../base_image_x64
sudo docker build . --tag=msh-x64:v0.0.1
# CREO ED ESEGUO IMMAGINE RASPBERRY ARM CON QEMU
cp ../../server ../raspberry_image_ARM
cd ../raspberry_image_ARM
sudo docker build . --build-arg google_actions_project_id=$1 --build-arg user=$2 --build-arg password=$3 --build-arg dominio_oauth=$4 --build-arg dominio_webapp=$5 --tag=raspberry-arm:v0.0.1
sudo docker run -d --name raspberry-arm raspberry-arm:v0.0.1
# CREO ED ESEGUO IMMAGINE RASPBERRY ARM SENZA QEMU
cp ../../server ../raspberry_image_ARM_prod
cd ../raspberry_image_ARM_prod
sudo docker build . --build-arg google_actions_project_id=$1 --build-arg user=$2 --build-arg password=$3 --build-arg dominio_oauth=$4 --build-arg dominio_webapp=$5 --tag=raspberry-arm-prod:v0.0.1
sudo docker run -d --name raspberry-arm-prod raspberry-arm-prod:v0.0.1
# CREO ED ESEGUO IMMAGINE RASPBERRY X64
cp ../../server ../raspberry_image_x64
cd ../raspberry_image_x64
sudo docker build . --build-arg google_actions_project_id=$1 --build-arg user=$2 --build-arg password=$3 --build-arg dominio_oauth=$4 --build-arg dominio_webapp=$5 --tag=raspberry-x64:v0.0.1
sudo docker run -d --name raspberry-x64 raspberry-x64:v0.0.1
