#!/bin/bash

# OPENSSH PER REMOTE SHUTDOWN
echo "Eseguo apt-get install openssh-server"
sudo apt-get install openssh-server -y 1>/dev/null
sudo rm /etc/ssh/ssh_host_* 1>/dev/null
echo "Eseguo dpkg-reconfigure openssh-server"
sudo dpkg-reconfigure openssh-server 1>/dev/null
echo "Eseguo service ssh start"
sudo service ssh start 1>/dev/null
echo "Imposto avvio servizio ssh all'avvio"
sudo update-rc.d ssh enable 1>/dev/null
#Per accesso root tramite ssh
#(Rimuovere without-password dopo:  PermitRootLogin, Aggiungere yes dopo: PermitRootLogin)
#sudo nano /etc/ssh/sshd_config

# WAKE ON LAN
#https://help.ubuntu.com/community/WakeOnLan
sudo apt-get install ethtool -y 1>/dev/null
#sudo ethtool eth0
#Se Supports Wake-on: pg OK
#Se Wake-on: d eseguire comando:
sudo ethtool -s eth0 wol g