#!/bin/bash

# UPDATE
sudo apt-get update -y
# APT-UTILS
sudo apt-get install apt-utils -y
# PS, TOP, ecc..
sudo apt-get install procps -y
# NETSTAT
sudo apt-get install net-tools -y
# CURL
sudo apt-get install curl -y
# NMAP
sudo apt-get install nmap -y
# SSH
sudo apt-get install ssh -y
# WAKEONLAN
sudo apt-get install wakeonlan -y
# SAMBA per comando NET
sudo apt-get install samba-common-bin -y
# NPM AND NGROK
curl -sL https://deb.nodesource.com/setup_6.x | sudo bash -
sudo apt-get install npm -y
# GACTIONS
sudo curl https://dl.google.com/gactions/updates/bin/linux/arm/gactions --output /usr/bin/gactions
sudo chmod +x /usr/bin/gactions
# PYTHON
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
pip3 install --trusted-host pypi.python.org webapp3
pip3 install --trusted-host pypi.python.org paste
pip3 install --trusted-host pypi.python.org pexpect
pip3 install --trusted-host pypi.python.org netifaces
# SQLITE
sudo apt-get install sqlite3 libsqlite3-dev -y
# SERVER APPLICATIVO
cd ..
mkdir msh/db
sqlite3 ./msh/db/system.db
sqlite3 ./msh/db/system.db < ../script/create.sql
python3 msh.py
# SERVER OAUTH
cd ../smarthome-androidthings-master/servers/fake-oauth-server-nodejs
# install solo la prima volta
npm install
npm start
# serve token al primo giro, account su ngrok da scrivere nello yaml
# SERVER NGROK
cd ../../../ngrock
./ngrok start --config=ngrok.yaml --all
# ogni volta che si ristarta bisogna cambiare gli URL nella action
# serve project ID
# GOOGLE ACTION creare action on google e recuperare project id, ingranaggio, project settings
cd ../msh
gactions update --action_package action.json --project smart-home-android-thing-deadd
# impostre credenziali Account Linking OAuth Authorization Code
# RKkWfsi0Z9
# eToBzeBT7OwrPQO8mZHsZtLp1qhQbe
# https://da88c583.ngrok.io/oauth va cambiato ogni volta che restarta ngrok
# https://da88c583.ngrok.io/token va cambiato ogni volta che restarta ngrok
