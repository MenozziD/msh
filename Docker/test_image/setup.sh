#!/bin/bash
echo "---------- START SETUP ----------"
# CAMBIO PASSWORD
echo "---------- CAMBIO PASSWORD ----------"
echo "Eseguo cambio password dell'utente pi, vecchia password: raspberry"
passwd
# CAMBIO PASSWORD ROOT
echo "Eseguo cambio password dell'utente root"
sudo passwd root
echo "---------- UPDATE/INSTALLAZIONE PACCHETTI ----------"
# UPDATE
echo "Eseguo apt-get update"
sudo apt-get update -y 1>/dev/null 
# UPGRADE
echo "Eseguo apt-get upgrade"
sudo apt-get upgrade -y 1>/dev/null 
# APT-UTILS
echo "Eseguo apt-get install apt-utils"
sudo apt-get install apt-utils -y 1>/dev/null 
# PS, TOP, ecc..
echo "Eseguo apt-get install procps"
sudo apt-get install procps -y 1>/dev/null 
# NETSTAT
echo "Eseguo apt-get install net-tools"
sudo apt-get install net-tools -y 1>/dev/null 
# CURL
echo "Eseguo apt-get install curl"
sudo apt-get install curl -y 1>/dev/null 
# NMAP
echo "Eseguo apt-get install nmap"
sudo apt-get install nmap -y 1>/dev/null 
# AUTOSSH
echo "Eseguo apt-get install autossh"
sudo apt-get install autossh 1>/dev/null 
# SSH CLIENT
echo "Eseguo apt-get install ssh"
sudo apt-get install ssh -y 1>/dev/null 
# SSH SERVER
echo "Eseguo apt-get install openssh-server"
sudo apt-get install openssh-server -y 1>/dev/null 
sudo rm /etc/ssh/ssh_host_* 1>/dev/null 
echo "Eseguo dpkg-reconfigure openssh-server"
sudo dpkg-reconfigure openssh-server 1>/dev/null
echo "Eseguo service ssh start"
sudo service ssh start 1>/dev/null 
# WAKEONLAN
echo "Eseguo apt-get install wakeonlan"
sudo apt-get install wakeonlan -y 1>/dev/null 
# SAMBA per comando NET
echo "Eseguo apt-get install samba-common-bin"
sudo apt-get install samba-common-bin -y 1>/dev/null 
# CRON
echo "Eseguo apt-get install cron"
sudo apt-get install cron -y 1>/dev/null 
echo "Eseguo service cron start"
sudo service cron start 1>/dev/null 
# GACTIONS
echo "Eseguo download di gactions in /usr/bin/gactions"
sudo curl https://dl.google.com/gactions/updates/bin/linux/arm/gactions --output /usr/bin/gactions 1>/dev/null 2>/dev/null
echo "Assegno permessi di esecuzione a gactions"
sudo chmod +x /usr/bin/gactions 
# NPM
echo "Aggiungo repository per apt-get"
sudo curl -sL https://deb.nodesource.com/setup_9.x | sudo bash - 1>/dev/null 2>/dev/null
echo "Eseguo apt-get install nodejs"
sudo apt-get install nodejs -y 1>/dev/null
# UNZIP
echo "Eseguo apt-get install unzip"
sudo apt-get install unzip -y 1>/dev/null
echo "Eseguo apt-get install zip"
sudo apt-get install zip -y 1>/dev/null
# PS4-WAKER
echo "Scarico ps4-waker.zip"
sudo curl https://codeload.github.com/dhleong/ps4-waker/zip/master --output /usr/lib/ps4-waker.zip 1>/dev/null 2>/dev/null
cd /usr/lib
echo "Eseguo unzip ps4-waker.zip"
sudo unzip ps4-waker.zip 1>/dev/null 2>/dev/null
echo "Eseguo mv ps4-waker-master ps4-waker"
sudo mv ps4-waker-master ps4-waker
echo "Eseguo mv ps4-waker/lib ps4-waker/dist"
sudo mv ps4-waker/lib ps4-waker/dist
echo "Installo ps4-waker"
sudo npm i ps4-waker -g
echo "Rimuovo ps4-waker.zip"
sudo rm -rf ps4waker.zip
cd /home/pi
# PYTHON
echo "Eseguo apt-get install python3"
sudo apt-get install python3 -y 1>/dev/null 
echo "Eseguo apt-get install python3-pip"
sudo apt-get install python3-pip -y 1>/dev/null 
echo "Eseguo pip3 install webapp3"
sudo pip3 install --trusted-host pypi.python.org webapp3 1>/dev/null 
echo "Eseguo pip3 install paste"
sudo pip3 install --trusted-host pypi.python.org paste 1>/dev/null 
echo "Eseguo pip3 install pexpect"
sudo pip3 install --trusted-host pypi.python.org pexpect 1>/dev/null
echo "Eseguo pip3 install netifaces" 
sudo pip3 install --trusted-host pypi.python.org netifaces 1>/dev/null 
echo "Eseguo pip3 install python-crontab" 
sudo pip3 install --trusted-host pypi.python.org python-crontab 1>/dev/null
echo "Eseguo pip3 install fritzconnection"
sudo pip3 install --trusted-host pypi.python.org fritzconnection 1>/dev/null
echo "Eseguo pip3 install requests"
sudo pip3 install --trusted-host pypi.python.org requests 1>/dev/null
# SQLITE
echo "Eseguo apt-get install sqlite3 libsqlite3-dev"
sudo apt-get install sqlite3 libsqlite3-dev -y 1>/dev/null 
# SET CRON E SSH START ON REBOOT
echo "Imposto avvio servizio cron all'avvio"
sudo update-rc.d cron enable 1>/dev/null
echo "Imposto avvio servizio ssh all'avvio"
sudo update-rc.d ssh enable 1>/dev/null
# SCARICO E CONFIGURO ARDUINO-CLI
echo "Eseguo download di arduino-cli.tar.bz2"
sudo curl "https://downloads.arduino.cc/arduino-cli/arduino-cli-latest-linuxarm.tar.bz2" --output arduino-cli.tar.bz2 1>/dev/null 2>/dev/null
echo "Decomprimo arduino-cli.tar.bz2"
sudo tar -xaf arduino-cli.tar.bz2 1>/dev/null
sudo rm -f arduino-cli.tar.bz2 1>/dev/null
echo "Sposto arduino-cli in /usr/bin/arduino-cli"
sudo mv arduino-cli-* /usr/bin/arduino-cli 1>/dev/null
echo "Creo configurazione per arduino-cli"
sudo su -c "arduino-cli config init 1>/dev/null"
sudo su -c "echo \"proxy_type: auto
sketchbook_path: /root/Arduino
arduino_data: /root/.arduino15
board_manager:
  additional_urls:
    - http://arduino.esp8266.com/stable/package_esp8266com_index.json\" >  /root/.arduino15/arduino-cli.yaml"
echo "Eseguo arduino-cli core update-index"
sudo arduino-cli core update-index 1>/dev/null
echo "Installo librerie Arduino per compilare"
echo "Install WiFi"
sudo arduino-cli lib install WiFi
echo "Install esp8266_mdns"
sudo arduino-cli lib install esp8266_mdns
echo "Install SimpleDHT"
sudo arduino-cli lib install SimpleDHT
echo "Install ArduinoJson"
sudo arduino-cli lib install ArduinoJson
# INSTALLAZIONE CORE SCHEDE
echo "Eseguo arduino-cli core install esp8266:esp8266"
sudo arduino-cli core install esp8266:esp8266 1>/dev/null
# AGGIUNGO 2 GB DI SWAP PER LA RAM
echo "---------- AGGIUNTA MEMORIA SWAP ----------"
echo "Modifico il file /etc/dphys-swapfile impostando dimensione partizione"
sudo echo "# where we want the swapfile to be, this is the default
#CONF_SWAPFILE=/var/swap

CONF_SWAPSIZE=2048

# set size to computed value, this times RAM size, dynamically adapts,
#   guarantees that there is enough swap without wasting disk space on excess
#CONF_SWAPFACTOR=2

#CONF_MAXSWAP=2048" > /etc/dphys-swapfile
echo "Restart servzio dphys-swapfile"
sudo /etc/init.d/dphys-swapfile restart 1>/dev/null
# SCARICO PAGEKITE
echo "Download di pagekite.py"
sudo curl https://pagekite.net/pk/pagekite.py --output server/pagekite.py 1>/dev/null 2>/dev/null
# SCARICO I SERVER
echo "Scarico server da GIT"
#sudo curl https://codeload.github.com/VanMenoz92/msh/zip/master --output msh.zip 1>/dev/null 2>/dev/null
sudo curl https://codeload.github.com/VanMenoz92/msh/zip/master --output msh.zip
sudo unzip msh.zip 1>/dev/null
sudo mv msh-master/server . 1>/dev/null
sudo rm -rf msh-master 1>/dev/null
sudo rm -rf msh.zip 1>/dev/null
echo "---------- LETTURA PARAMETRI ----------"
read -p "Inserire un USERNAME per applicazione (es. simone): " USERNAME
read -p "Inserire la PASSWORD per l'utente $USERNAME: " PASSWORD
