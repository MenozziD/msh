#!/bin/bash

# CONFIGURARE IL LAYOUT DELLA TASTIERA ---> sudo dpkg-reconfigure keyboard-configuration
# RESTART DEL SERVIZIO TASTIERA ----------> sudo service keyboard-setup restart
# CONFIGURARE TIME ZONE ------------------> sudo dpkg-reconfigure tzdata
# ABILITARE SSH PER UTENTE ROOT ----------> sudo nano /etc/ssh/sshd_config
# SCARICA SCRIPT -------------------------> sudo curl https://raw.githubusercontent.com/VanMenoz92/msh/master/script/setup/01_setup.sh --output 01_setup.sh
# ABILITARE ESECUZIONE PER LO SCRIPT -----> sudo chmod 744 01_setup.sh
# ESEGUIRE LO SCRIPT ---------------------> sudo ./01_setup.sh

#CHECK WIFI
WIFI=false
if [ "$#" -ne 2 ]; then
  echo "Non verra configurato il Wi-Fi"
else
  echo "Verra configurato il Wi-Fi"
  WIFI=true
fi
# ABILITO WIFI
if [ "$WIFI" == true ]; then
	echo "---------- CONFIGURAZIONE WIFI ----------"
	echo "Scrivo file delle interfacce di rete al path /etc/network/interfaces"
	sudo echo "auto lo

iface lo inet loopback
iface eth0 inet dhcp

auto wlan0
iface wlan0 inet dhcp
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf" > /etc/network/interfaces
	sudo mkdir /etc/wpa_supplicant/
	echo "Scrivo file di configurazione per l'interfaccia wlan0 al path /etc/wpa_supplicant/wpa_supplicant.conf"
	sudo echo "ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
update_config=1

network={
        ssid=\"$1\"
        psk=\"$2\"
        proto=WPA
        key_mgmt=WPA-PSK
        pairwise=TKIP
        group=TKIP
        id_str=\"$1\"
}" > /etc/wpa_supplicant/wpa_supplicant.conf
# RESTART DEL SERVIZIO PER FARGLI LEGGERE LE CONFIGURAZIONI
	echo "Eseguo restart del servizio networking"
	sudo /etc/init.d/networking restart
fi
# CAMBIO PASSWORD
echo "---------- CAMBIO PASSWORD ----------"
echo "Eseguo cambio password dell'utente pi, vecchia password: raspberry"
sudo passwd
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
sudo curl https://dl.google.com/gactions/updates/bin/linux/arm/gactions --output /usr/bin/gactions 1>/dev/null 
echo "Assegno permessi di esecuzione a gactions"
sudo chmod +x /usr/bin/gactions 
# NPM
echo "Aggiungo repository per apt-get"
sudo curl -sL https://deb.nodesource.com/setup_6.x | sudo bash - 1>/dev/null 
echo "Eseguo apt-get install npm"
sudo apt-get install npm -y 1>/dev/null 
# UNZIP
echo "Eseguo apt-get install unzip"
sudo apt-get install unzip -y 1>/dev/null
echo "Eseguo apt-get install zip"
sudo apt-get install zip -y 1>/dev/null
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
# SQLITE
echo "Eseguo apt-get install sqlite3 libsqlite3-dev"
sudo apt-get install sqlite3 libsqlite3-dev -y 1>/dev/null 
# SET CRON E SSH START ON REBOOT
echo "Imposto avvio servizio cron all'avvio"
sudo update-rc.d cron enable 1>/dev/null
echo "Imposto avvio servizio ssh all'avvio"
sudo update-rc.d ssh enable 1>/dev/null
#SCARICO E CONFIGURO ARDUINO-CLI
echo "Eseguo download di arduino-cli.tar.bz2"
sudo curl "https://downloads.arduino.cc/arduino-cli/arduino-cli-latest-linuxarm.tar.bz2" --output arduino-cli.tar.bz2 1>/dev/null
echo "Decomprimo arduino-cli.tar.bz2"
sudo tar -xaf arduino-cli.tar.bz2 1>/dev/null
sudo rm -f arduino-cli.tar.bz2 1>/dev/null
echo "Sposto arduino-cli in /usr/bin/arduino-cli"
sudo mv arduino-cli-* /usr/bin/arduino-cli 1>/dev/null
echo "Creo configurazione per arduino-cli"
sudo arduino-cli config init 1>/dev/null
sudo su 1>/dev/null
echo "proxy_type: auto
sketchbook_path: /root/Arduino
arduino_data: /root/.arduino15
board_manager:
  additional_urls:
    - http://arduino.esp8266.com/stable/package_esp8266com_index.json" >  /root/.arduino15/arduino-cli.yaml
echo "Eseguo arduino-cli core update-index"
sudo arduino-cli core update-index 1>/dev/null
#INSTALLAZIONE CORE SCHEDE
echo "Eseguo arduino-cli core install esp8266:esp8266"
sudo arduino-cli core install esp8266:esp8266 1>/dev/null
# AGGIUNGO 2 GB DI SWAP PER LA RAM
echo "---------- AGGIUNTA MEMORIA SWAP ----------"
echo "Creo file da 2GB per swap in /root/swapfile"
sudo dd if=/dev/zero of=/root/swapfile bs=1M count=2048 1>/dev/null
echo "Imposto permessi sul file /root/swapfile"
sudo chmod 600 /root/swapfile 1>/dev/null
echo "Eseguo mkswap /root/swapfile"
sudo mkswap /root/swapfile 1>/dev/null
echo "Eseguo swapon /root/swapfile"
sudo swapon /root/swapfile 1>/dev/null
# SCARICO I SERVER E IL SECONDO SETUP
echo "---------- PREPARAZIONE SECONDA INSTALLAZIONE ----------"
echo "Scarico il secondo setup"
sudo curl https://raw.githubusercontent.com/VanMenoz92/msh/master/script/setup/02_setup.sh --output 02_setup.sh 1>/dev/null
echo "Assegno permessi di esecuzione al nuovo setup"
sudo chmod 744 02_setup.sh 1>/dev/null
echo "Scarico server da GIT"
sudo curl https://codeload.github.com/VanMenoz92/msh/zip/master --output msh.zip 1>/dev/null
sudo unzip msh.zip 1>/dev/null
sudo mv msh-master/server . 1>/dev/null
sudo rm -rf msh-master 1>/dev/null
sudo rm -rf msh.zip 1>/dev/null
echo "---------- TO DO ----------"
echo "1) Accedere all'URL https://console.actions.google.com/ e creare un nuovo progetto"
echo "2) Accedere alla voce project settings e copiare il project ID"
echo "3) Eseguire il comando sudo ./02_setup.sh GOOGLE_PROJECT_ID USERNAME_WEBAPP PASSWORD_WEBAPP DOMINIO_OAUTH DOMINIO_WEBAPP"
exit 0
