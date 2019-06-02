#!/bin/bash

if [ "$#" -ne 7 ]; then
  echo "Usage: $0 GOOGLE_PROJECT_ID USERNAME PASSWORD DOMINIO_OAUTH DOMINIO_WEBAPP NAME_WIFI PASSWORD_WIFI" >&2
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
apt-get install qemu-user-static -y
# CREO IMMAGINE BASE ARM CON QEMU
cd ../Docker/base_image_ARM
sudo ./deploy.sh
# CREO IMMAGINE BASE X64
cd ../base_image_x64
sudo ./deploy.sh
# CREO ED ESEGUO IMMAGINE RASPBERRY ARM CON QEMU
cd ../raspberry_image_ARM
sudo ./deploy.sh $1 $2 $3 $4 $5 $6 $7
# CREO ED ESEGUO IMMAGINE RASPBERRY X64
cd ../raspberry_image_x64
sudo ./deploy.sh $1 $2 $3 $4 $5 $6 $7
