#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 NGROK_AUTHTOKEN GOOGLE_PROJECT_ID" >&2
  exit 1
fi

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
# NPM
sudo curl -sL https://deb.nodesource.com/setup_6.x | sudo bash -
sudo apt-get install npm -y
# UNZIP
sudo apt-get install unzip -y
# NGROK
sudo curl https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip --output /usr/bin/ngrok-stable-linux-arm.zip
sudo unzip /usr/bin/ngrok-stable-linux-arm.zip -d /usr/bin
sudo rm /usr/bin/ngrok-stable-linux-arm.zip
# GACTIONS
sudo curl https://dl.google.com/gactions/updates/bin/linux/arm/gactions --output /usr/bin/gactions
sudo chmod +x /usr/bin/gactions
# PYTHON
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo pip3 install --trusted-host pypi.python.org webapp3
sudo pip3 install --trusted-host pypi.python.org paste
sudo pip3 install --trusted-host pypi.python.org pexpect
sudo pip3 install --trusted-host pypi.python.org netifaces
# SQLITE
sudo apt-get install sqlite3 libsqlite3-dev -y
# DATABASE
cd ../server
mkdir msh/db
sudo sqlite3 ./msh/db/system.db
sudo sqlite3 ./msh/db/system.db < ./msh/script/create.sql
# SERVER OAUTH
cd fake-oauth-server-nodejs
sudo npm install
# CREO NGROK.YAML CON TOKEN PRESO IN INPUT
echo "authtoken: $1
tunnels:
  app-foo:
    addr: 65177
    proto: http
  app-bar:
    addr: 3000
    proto: http" > ../ngrok/ngrok.yaml
# SALVO PROJECT ID DI GOOGLE ACTIONS IN SETTINGS.XML
echo "<settings>
	<porta>65177</porta>
	<lingua>IT</lingua>
	<timestamp>%Y-%m-%d %H:%M:%S</timestamp>
	<project_id_google_actions>$2</project_id_google_actions>
	<log>
		<!-- Se valorizzato con None logga in console -->
		<filename>msh.log</filename>
		<format>%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s</format>
		<!-- debug, info, warning, error, critical -->
		<level>info</level>
	</log>
</settings>" > ../msh/settings.xml
echo "impostare credenziali Account Linking | OAuth | Authorization Code | client ID RKkWfsi0Z9"
echo "impostare credenziali Account Linking | OAuth | Authorization Code | client secret eToBzeBT7OwrPQO8mZHsZtLp1qhQbe"
cd ..