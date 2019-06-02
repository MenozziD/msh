#!/bin/bash

if [ "$#" -ne 7 ]; then
  echo "Usage: $0 GOOGLE_PROJECT_ID USERNAME_WEBAPP PASSWORD_WEBAPP DOMINIO_OAUTH DOMINIO_WEBAPP NOME_WIFI PASSWORD_WIFI" >&2
  exit 1
fi

# ABILITO WIFI
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
        ssid=\"$6\"
        psk=\"$7\"
        proto=WPA
        key_mgmt=WPA-PSK
        pairwise=TKIP
        group=TKIP
        id_str=\"$6\"
}" > /etc/wpa_supplicant/wpa_supplicant.conf
sudo echo "{
	\"actions\": [{
			\"fulfillment\": {
				\"conversationName\": \"automation\"
			},
			\"name\": \"actions.devices\"
		}
	],
	\"conversations\": {
		\"automation\": {
			\"name\": \"automation\",
			\"url\": \"https://$5.serveo.net/api/home\"
		}
	},
	\"locale\": \"it\"
}" > action.json
# CREO GACTIONS
#OK=false
#while [ "$OK" == false ]
#do	
#	if gactions update --action_package action.json --project $1
#	then
#		OK=true
#	fi
#done
# DATABASE
cd server
mkdir msh/db
sudo sqlite3 ./msh/db/system.db
sudo sqlite3 ./msh/db/system.db < ./msh/script/create.sql
sudo echo "INSERT INTO TB_USER (USERNAME, PASSWORD, ROLE) VALUES ('$2', '$3', 'ADMIN');" > ./msh/script/user.sql
sudo sqlite3 ./msh/db/system.db < ./msh/script/user.sql
# SERVER OAUTH
cd oauth
python3 oauth.py
token=`cat token.txt`
client_id=`cat clientid.txt`
client_secret=`cat clientsecret.txt`
rm -f token.txt
rm -f clientid.txt
rm -f clientsecret.txt
rm -f token.txt
echo "const Data = {};

const Auth = {
  clients: {
    '$client_id': {
      clientId: '$client_id',
      clientSecret: '$client_secret'
    }
  },
  tokens: {
    '$token': {
      uid: '1',
      accessToken: '$token',
      refreshToken: '$token',
      userId: '1'
    }
  },
  users: {
    '1': {
      uid: '1',
      name: '$3',
      password: '$4',
      tokens: ['$token']
    }
  },
  usernames: {
    '$3': '1'
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
# SALVO PROJECT ID DI GOOGLE ACTIONS IN SETTINGS.XML
echo "<settings>
	<lingua>IT</lingua>
	<timestamp>%Y-%m-%d %H:%M:%S</timestamp>
	<project_id_google_actions>$1</project_id_google_actions>
	<subdomain_oauth>$4</subdomain_oauth>
	<subdomain_webapp>$5</subdomain_webapp>
	<log>
		<!-- Se valorizzato con None logga in console -->
		<filename>msh.log</filename>
		<format>%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s</format>
		<!-- debug, info, warning, error, critical -->
		<level>info</level>
	</log>
</settings>" > ../msh/settings.xml
echo "impostare credenziali Account Linking | OAuth | Authorization Code | Client ID: $client_id"
echo "impostare credenziali Account Linking | OAuth | Authorization Code | Client secret: $client_secret"
echo "impostare credenziali Account Linking | OAuth | Authorization Code | Authorization URL: https://$4.serveo.net/oauth" 
echo "impostare credenziali Account Linking | OAuth | Authorization Code | Token URL: https://$4.serveo.net/token"
cd ../msh
#sudo python3 msh.py 2> /dev/null &
#if curl -I -X GET http://127.0.0.1:65177/static/page/login.html | grep 200
#then
#	echo "INSTALLAZIONE RIUSCITA!!"
#else
#	echo "INSTALLAZIONE KO!!"
#fi
