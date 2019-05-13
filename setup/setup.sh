#!/bin/bash

# UPDATE
apt-get update -y
# APT-UTILS
apt-get install apt-utils -y
# PS, TOP, ecc..
apt-get install procps -y
# NETSTAT
apt-get install net-tools -y
# CURL
apt-get install curl -y
# NMAP
apt-get install nmap -y
# SSH
apt-get install ssh -y
# WAKEONLAN
apt-get install wakeonlan -y
# SAMBA per comando NET
apt-get install samba-common-bin -y
# PYTHON
apt-get install python3 -y
apt-get install python3-pip -y
pip3 install --trusted-host pypi.python.org webapp3
pip3 install --trusted-host pypi.python.org paste
pip3 install --trusted-host pypi.python.org pexpect
# SQLITE
apt-get install sqlite3 libsqlite3-dev -y
# SUDO
apt-get install sudo -y

cd ../msh
mkdir db
cd db
sqlite3 ./system.db
sqlite3 ./system.db < ../script/create.sql
python3 msh.py
if curl -I -X GET http://127.0.0.1:80/static/page/index.html | grep 200;
	then
		echo "INSTALLAZIONE RIUSCITA!!"
	else
		echo "INSTALLAZIONE KO!!"
fi
