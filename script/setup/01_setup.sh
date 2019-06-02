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
# SSH CLIENT
sudo apt-get install opessh-client -y
# SSH SERVER
sudo apt-get install openssh-server -y
sudo rm /etc/ssh/ssh_host_*
sudo dpkg-reconfigure openssh-server
sudo service ssh start
# WAKEONLAN
sudo apt-get install wakeonlan -y
# SAMBA per comando NET
sudo apt-get install samba-common-bin -y
# CRON
sudo apt-get install cron -y
sudo service cron start
# GACTIONS
# sudo curl https://dl.google.com/gactions/updates/bin/linux/arm/gactions --output /usr/bin/gactions
# sudo chmod +x /usr/bin/gactions
# NPM
sudo curl -sL https://deb.nodesource.com/setup_6.x | sudo bash -
sudo apt-get install npm -y
# UNZIP
sudo apt-get install unzip -y
# PYTHON
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo pip3 install --trusted-host pypi.python.org webapp3
sudo pip3 install --trusted-host pypi.python.org paste
sudo pip3 install --trusted-host pypi.python.org pexpect
sudo pip3 install --trusted-host pypi.python.org netifaces
sudo pip3 install --trusted-host pypi.python.org python-crontab
# SQLITE
sudo apt-get install sqlite3 libsqlite3-dev -y
# SET CRON E SSH START ON REBOOT
sudo update-rc.d cron enable
sudo update-rc.d ssh enable
