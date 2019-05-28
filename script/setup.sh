#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 NGROK_AUTHTOKEN GOOGLE_PROJECT_ID USERNAME PASSWORD" >&2
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
# CRON
sudo apt-get install cron -y
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
sudo pip3 install --trusted-host pypi.python.org python-crontab
# SQLITE
sudo apt-get install sqlite3 libsqlite3-dev -y
# DATABASE
cd ../server
mkdir msh/db
sudo sqlite3 ./msh/db/system.db
sudo sqlite3 ./msh/db/system.db < ./msh/script/create.sql
sudo echo "INSERT INTO TB_USER (USERNAME, PASSWORD, ROLE) VALUES ('$3', '$4', 'ADMIN');" > ./msh/script/user.sql
sudo sqlite3 ./msh/db/system.db < ./msh/script/user.sql
# SERVER OAUTH
cd fake-oauth-server-nodejs
echo "const Data = {};

const Auth = {
  clients: {
    'RKkWfsi0Z9': {
      clientId: 'RKkWfsi0Z9',
      clientSecret: 'eToBzeBT7OwrPQO8mZHsZtLp1qhQbe'
    }
  },
  tokens: {
    'psokmCxKjfhk7qHLeYd1': {
      uid: '1234',
      accessToken: 'psokmCxKjfhk7qHLeYd1',
      refreshToken: 'psokmCxKjfhk7qHLeYd1',
      userId: '1234'
    }
  },
  users: {
    '1234': {
      uid: '1234',
      name: '$3',
      password: '$4',
      tokens: ['psokmCxKjfhk7qHLeYd1']
    }
  },
  usernames: {
    '$3': '1234'
  },
  authcodes: {}
};

Data.version = 0;

Data.getUid = function (uid) {
  return Data[uid];
};

/**
 * checks if user and auth exist and match
 *
 * @param uid
 * @param authToken
 * @returns {boolean}
 */
Data.isValidAuth = function (uid, authToken) {
  return (Data.getUid(uid));
};

exports.getUid = Data.getUid;
exports.isValidAuth = Data.isValidAuth;
exports.Auth = Auth;" > datastore.js
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