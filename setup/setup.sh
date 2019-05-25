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
sudo npm install ngrok -g
# GACTIONS
curl https://dl.google.com/gactions/updates/bin/linux/arm/gactions --output /usr/bin/gactions
chmod +x /usr/bin/gactions
# PYTHON
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
pip3 install --trusted-host pypi.python.org webapp3
pip3 install --trusted-host pypi.python.org paste
pip3 install --trusted-host pypi.python.org pexpect
pip3 install --trusted-host pypi.python.org netifaces
# SQLITE
sudo apt-get install sqlite3 libsqlite3-dev -y

cd ../msh
mkdir db
cd db
sqlite3 ./system.db
sqlite3 ./system.db < ../script/create.sql
python3 msh.py