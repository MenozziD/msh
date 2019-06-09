#!/bin/bash

WIFI=false
if [ "$#" -ne 2 ]; then
  echo "Non verra configurato il Wi-Fi"
else
  echo "Verra configurato il Wi-Fi"
  WIFI=true
fi

# CONFIGURARE IL LAYOUT DELLA TASTIERA ---> sudo dpkg-reconfigure keyboard-configuration
# RESTART DEL SERVIZIO TASTIERA ----------> sudo service keyboard-setup restart
# CONFIGURARE TIME ZONE ------------------> sudo dpkg-reconfigure tzdata
# SCARICA SCRIPT -------------------------> sudo curl https://raw.githubusercontent.com/VanMenoz92/msh/master/script/setup/01_setup.sh --output 01_setup.sh
# ABILITARE ESECUZIONE PER LO SCRIPT -----> sudo chmod 744 01_setup.sh
# ESEGUIRE LO SCRIPT ---------------------> sudo ./01_setup.sh

# ABILITO WIFI
if [ "$WIFI" == true ]; then
	sudo echo "auto lo

iface lo inet loopback
iface eth0 inet dhcp

auto wlan0
iface wlan0 inet dhcp
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf" > /etc/network/interfaces
	sudo mkdir /etc/wpa_supplicant/
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
fi
# RESTART DEL SERVIZIO PER FARGLI LEGGERE LE CONFIGURAZIONI
sudo /etc/init.d/networking restart
# UPDATE
sudo apt-get update -y
# UPGRADE
sudo apt-get upgrade -y
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
# AUTOSSH
sudo apt-get install autossh
# SSH CLIENT
sudo apt-get install ssh -y
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
sudo curl https://dl.google.com/gactions/updates/bin/linux/arm/gactions --output /usr/bin/gactions
sudo chmod +x /usr/bin/gactions
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
#SCARICO E CONFIGURO ARDUINO-CLI
sudo curl "https://downloads.arduino.cc/arduino-cli/arduino-cli-latest-linuxarm.tar.bz2" --output arduino-cli.tar.bz2
sudo tar -xaf arduino-cli.tar.bz2
sudo rm -f arduino-cli.tar.bz2
sudo mv arduino-cli-* /usr/bin/arduino-cli
sudo arduino-cli config init
sudo su
echo "proxy_type: auto
sketchbook_path: /root/Arduino
arduino_data: /root/.arduino15
board_manager:
  additional_urls:
    - http://arduino.esp8266.com/stable/package_esp8266com_index.json" >  /root/.arduino15/arduino-cli.yaml
sudo arduino-cli core update-index
#INSTALLAZIONE CORE SCHEDE
sudo arduino-cli core install esp8266:esp8266
# AGGIUNGO 2 GB DI SWAP PER LA RAM
sudo dd if=/dev/zero of=/root/swapfile bs=1M count=2048
sudo chmod 600 /root/swapfile
sudo mkswap /root/swapfile
sudo swapon /root/swapfile
# SCARICO I SERVER E IL SECONDO SETUP
sudo curl https://raw.githubusercontent.com/VanMenoz92/msh/master/script/setup/02_setup.sh --output 02_setup.sh
sudo chmod 744 02_setup.sh
sudo curl https://codeload.github.com/VanMenoz92/msh/zip/master --output msh.zip
sudo unzip msh.zip 1>/dev/null 2>/dev/null
sudo mv msh-master/server .
sudo rm -rf msh-master
sudo rm -rf msh.zip
exit 0