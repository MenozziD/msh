#!/bin/bash
echo "---------- START SETUP ----------"
# APT UTILS, DIALOG
echo "Eseguo apt-get install dialog apt-utils"
sudo apt-get install dialog apt-utils -y 1>/dev/null
# CAMBIO PASSWORD
echo "---------- CAMBIO PASSWORD ----------"
printf "Eseguo cambio password dell'utente pi\nNuova password: a"
(echo 'a'; echo 'a') | passwd
# CAMBIO PASSWORD ROOT
printf "Eseguo cambio password dell'utente root\nNuova password: a"
(echo 'a'; echo 'a') | sudo passwd root
echo "---------- UPDATE/INSTALLAZIONE PACCHETTI ----------"
# UPDATE
echo "Eseguo apt-get update"
sudo apt-get update -y 1>/dev/null 
# UPGRADE
echo "Eseguo apt-get upgrade"
sudo apt-get upgrade -y 1>/dev/null 
# PS, TOP, NETSTAT, CURL, NMAP, AUTOSSH, SSH CLIENT, SSH SERVER, WAKEONLAN, SAMBA, CRON, PYTHON 3, PIP, SQLITE
echo "Eseguo apt-get install procps net-tools curl nmap autossh ssh openssh-server wakeonlan samba-common-bin cron python3 python3-pip sqlite3 libsqlite3-dev"
sudo apt-get install procps net-tools curl nmap autossh ssh openssh-server wakeonlan samba-common-bin cron python3 python3-pip sqlite3 libsqlite3-dev -y 1>/dev/null
# NPM
echo "Aggiungo repository per apt-get"
sudo curl -sL https://deb.nodesource.com/setup_9.x | sudo bash - 1>/dev/null
echo "Eseguo apt-get install build-essential nodejs npm unzip zip"
sudo apt-get install build-essential nodejs npm unzip zip -y 1>/dev/null
# PYTHON
echo "Eseguo pip3 install webapp3 paste pexpect netifaces python-crontab fritzconnection requests"
sudo pip3 install --trusted-host pypi.python.org webapp3 paste pexpect netifaces python-crontab fritzconnection requests 1>/dev/null 
# SET CRON E SSH START ON REBOOT
echo "Imposto avvio servizio cron all'avvio"
sudo update-rc.d cron enable 1>/dev/null
echo "Imposto avvio servizio ssh all'avvio"
sudo update-rc.d ssh enable 1>/dev/null
exit 0