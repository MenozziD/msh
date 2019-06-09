#!/bin/bash

if [ "$#" -ne 5 ]; then
  echo "Usage: $0 GOOGLE_PROJECT_ID USERNAME_WEBAPP PASSWORD_WEBAPP DOMINIO_OAUTH DOMINIO_WEBAPP" >&2
  exit 1
fi

#RIMUOVO PRIMO SETUP
sudo rm -rf 01_setup.sh
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
OK=false
while [ "$OK" == false ]
do	
	if gactions update --action_package action.json --project $1
	then
		OK=true
	fi
done
sudo rm -f action.json 
sudo rm -f creds.data
# DATABASE
cd server
mkdir msh/db
sudo sqlite3 ./msh/db/system.db < ./msh/script/create.sql
sudo echo "INSERT INTO TB_USER (USERNAME, PASSWORD, ROLE) VALUES ('$2', '$3', 'ADMIN');" > ./msh/script/user.sql
sudo sqlite3 ./msh/db/system.db < ./msh/script/user.sql
sudo rm -rf ./msh/script
# SERVER OAUTH
cd oauth
sudo echo "from string import ascii_letters, digits
from random import choice


def main():
    token = ''.join(choice(ascii_letters + digits) for i in range(36))
    f = open(\"token.txt\", \"w\")
    f.write(token)
    f.close()
    client_id = ''.join(choice(ascii_letters + digits) for i in range(32))
    f = open(\"clientid.txt\", \"w\")
    f.write(client_id)
    f.close()
    client_secret = ''.join(choice(ascii_letters + digits) for i in range(36))
    f = open(\"clientsecret.txt\", \"w\")
    f.write(client_secret)
    f.close()


if __name__ == '__main__':
    main()" > oauth.py
python3 oauth.py
token=`cat token.txt`
client_id=`cat clientid.txt`
client_secret=`cat clientsecret.txt`
rm -f token.txt
rm -f clientid.txt
rm -f clientsecret.txt
rm -f token.txt
rm -f oauth.py
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
      name: '$2',
      password: '$3',
      tokens: ['$token']
    }
  },
  usernames: {
    '$2': '1'
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
echo "Impostare credenziali Account Linking | OAuth | Authorization Code
Client ID: $client_id
Client secret: $client_secret
Authorization URL: https://$4.serveo.net/oauth
Token URL: https://$4.serveo.net/token"
cd ../..
echo '#!/bin/bash
### BEGIN INIT INFO
# Provides:          msh
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog  
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Servizio MSH
# Description:       Servizio MSH
### END INIT INFO

case "$1" in
start)  if [ $(pgrep python) ]
		then
			echo "Servizio MSH attivo"
		else
			cd /home/pi/server/msh && sudo python3 msh.py 1>/dev/null 2>/dev/null &
			echo "Avviato servizio MSH"
		fi
		;;
stop)   if [ $(pgrep python) ]
		then
			pgrep python | sudo kill -9 1>/dev/null 2>/dev/null
			echo \"Stoppato servizio MSH\"
		else
			echo "Servizio MSH non attivo"
		fi
        ;;
restart) if [ $(pgrep python) ]
		 then
			pgrep python | sudo kill -9 1>/dev/null 2>/dev/null
			cd /home/pi/server/msh && sudo python3 msh.py 1>/dev/null 2>/dev/null &
			echo "Restart servizio MSH"
		else
			echo "Servizio MSH non attivo"
		fi
        ;;
*)      echo "Usage: $0 {start|stop|restart}"
        exit 2
        ;;
esac
exit 0' > msh.sh
sudo mv msh.sh /etc/init.d/msh
sudo chmod +x /etc/init.d/msh
sudo service msh start
sudo update-rc.d msh enable
sleep 10
if curl -I -X GET http://127.0.0.1:65177/static/page/login.html | grep 200
then
	echo "INSTALLAZIONE RIUSCITA!!"
else
	echo "INSTALLAZIONE KO!!"
fi
exit 0