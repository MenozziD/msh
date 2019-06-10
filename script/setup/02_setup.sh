#!/bin/bash

if [ "$#" -ne 5 ]; then
  echo "Usage: $0 GOOGLE_PROJECT_ID USERNAME_WEBAPP PASSWORD_WEBAPP DOMINIO_OAUTH DOMINIO_WEBAPP" >&2
  exit 1
fi
# CHECK SUL DOMINIO_OAUTH E DOMINIO_WEBAPP
OAUTH=false
OAUTH_DOMAIN=$4
while [ "$OAUTH" == false ]
do
	echo "Verifico la disponibilita del dominio $OAUTH_DOMAIN"
	if curl -I -X GET https://$OAUTH_DOMAIN.serveo.net/ | grep "502 Bad Gateway"
	then
		echo "Dominio OAUTH disponibile"
		OAUTH=true
	else
		echo "Dominio OAUTH non disponibile"
		read -p "Inserire un nuovo dominio per OAUTH: " OAUTH_DOMAIN
	fi
done
WEBAPP=false
WEBAPP_DOMAIN=$5
while [ "$WEBAPP" == false ]
do
	echo "Verifico la disponibilita del dominio $WEBAPP_DOMAIN"
	if curl -I -X GET https://$WEBAPP_DOMAIN.serveo.net/ | grep "502 Bad Gateway"
	then
		echo "Dominio WEBAPP disponibile"
		WEBAPP=true
	else
		echo "Dominio WEBAPP non disponibile"
		read -p "Inserire un nuovo dominio per la WEBAPP: " WEBAPP_DOMAIN
	fi
done
#RIMUOVO PRIMO SETUP
echo "Rimuovo vecchio setup"
sudo rm -rf 01_setup.sh
# CREO GACTIONS
echo "Creo file action.json"
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
			\"url\": \"https://$WEBAPP_DOMAIN.serveo.net/api/home\"
		}
	},
	\"locale\": \"it\"
}" > action.json
echo "Eseguo update gactions"
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
echo "Creo cartella per il database"
mkdir msh/db
echo "Eseguo script di create"
sudo sqlite3 ./msh/db/system.db < ./msh/script/create.sql
echo "Creo script di insert"
sudo echo "INSERT INTO TB_USER (USERNAME, PASSWORD, ROLE) VALUES ('$2', '$3', 'ADMIN');" > ./msh/script/user.sql
echo "Eseguo script di insert"
sudo sqlite3 ./msh/db/system.db < ./msh/script/user.sql
echo "Rimuovo cartella script"
sudo rm -rf ./msh/script
# SERVER OAUTH
cd oauth
echo "Creo script python per generazione token"
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
echo "Eseguo script python per generazione token"
python3 oauth.py
token=`cat token.txt`
client_id=`cat clientid.txt`
client_secret=`cat clientsecret.txt`
echo "Rimuovo file temporanei"
rm -f token.txt
rm -f clientid.txt
rm -f clientsecret.txt
rm -f token.txt
rm -f oauth.py
echo "Creo datastore.js"
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
echo "Eseguo npm install"
sudo npm install 1>/dev/null 2>/dev/null
# SALVO PROJECT ID DI GOOGLE ACTIONS IN SETTINGS.XML
echo "Creo settings.xml"
echo "<settings>
	<lingua>IT</lingua>
	<timestamp>%Y-%m-%d %H:%M:%S</timestamp>
	<project_id_google_actions>$1</project_id_google_actions>
	<subdomain_oauth>$OAUTH_DOMAIN</subdomain_oauth>
	<subdomain_webapp>$WEBAPP_DOMAIN</subdomain_webapp>
	<log>
		<!-- Se valorizzato con None logga in console -->
		<filename>msh.log</filename>
		<format>%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s</format>
		<!-- debug, info, warning, error, critical -->
		<level>info</level>
	</log>
</settings>" > ../msh/settings.xml
cd ../..
# SERVIZIO OAUTH
echo "Creo script oauth.sh"
echo $'#!/bin/bash
### BEGIN INIT INFO
# Provides:          oauth
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Servizio OAUTH
# Description:       Servizio OAUTH
### END INIT INFO

case "$1" in
start)  if [ $(pgrep node) ]
                then
                        echo "Servizio OAUTH attivo"
                else
                        cd /home/pi/server/oauth && sudo npm start 1>/dev/null 2>/dev/null &
                        echo "Avviato servizio OAUTH"
                fi
                ;;
stop)   if [ $(pgrep node) ]
                then
                        pgrep node | awk \'{print $0}\' | xargs sudo kill -9 1>/dev/null 2>/dev/null
                        echo "Stoppato servizio OAUTH"
                else
                        echo "Servizio OAUTH non attivo"
                fi
        ;;
restart) if [ $(pgrep node) ]
                 then
                        pgrep node | awk \'{print $0}\' | xargs sudo kill -9 1>/dev/null 2>/dev/null
                        cd /home/pi/server/oauth && npm start 1>/dev/null 2>/dev/null &
                        echo "Restart servizio OAUTH"
                else
                        cd /home/pi/server/oauth && sudo npm start 1>/dev/null 2>/dev/null &
                        echo "Avviato servizio OAUTH"
                fi
        ;;
*)      echo "Usage: $0 {start|stop|restart}"
        exit 2
        ;;
esac
exit 0' > oauth.sh
echo "Sposto script oauth.sh in /etc/init.d/oauth"
sudo mv oauth.sh /etc/init.d/oauth
echo "Assegno permessi di esecuzione a /etc/init.d/oauth"
sudo chmod +x /etc/init.d/oauth 1>/dev/null
echo "Eseguo systemctl enable oauth"
sudo systemctl enable oauth 1>/dev/null 2>/dev/null
echo "Eseguo service oauth start"
sudo service oauth start 1>/dev/null
echo "Imposto avvio servizio oauth all'avvio"
sudo update-rc.d oauth enable 1>/dev/null
# SERVIZIO SERVEO
echo "Creo script serveo.sh"
echo $'#!/bin/bash
### BEGIN INIT INFO
# Provides:          serveo
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Servizio SERVEO
# Description:       Servizio SERVEO
### END INIT INFO

case "$1" in
start)  if [ $(pgrep autossh) ]
                then
						echo "Servizio SERVEO attivo"
                else
                        oauth=`cat /home/pi/server/msh/settings.xml | grep oauth | cut -d\'>\' -f 2 | cut -d\'<\' -f 1`
						webapp=`cat /home/pi/server/msh/settings.xml | grep webapp | cut -d\'>\' -f 2 | cut -d\'<\' -f 1`
                        autossh -M 0 -o "StrictHostKeyChecking no" -R $webapp:80:localhost:65177 -R $oauth:80:localhost:3000 serveo.net 1>/dev/null 2>/dev/null &
                        echo "Avviato servizio SERVEO"
                fi
                ;;
stop)   if [ $(pgrep autossh) ]
                then
                        pgrep autossh | awk \'{print $0}\' | xargs sudo kill -9 1>/dev/null 2>/dev/null
						ps -aux | grep serveo | grep localhost | awk \'{print $2}\' | xargs sudo kill -9 1>/dev/null 2>/dev/null
                        echo "Stoppato servizio SERVEO"
                else
                        echo "Servizio SERVEO non attivo"
                fi
        ;;
restart) if [ $(pgrep autossh) ]
                 then
                        pgrep autossh | awk \'{print $0}\' | xargs sudo kill -9 1>/dev/null 2>/dev/null
                        ps -aux | grep serveo | grep localhost | awk \'{print $2}\' | xargs sudo kill -9 1>/dev/null 2>/dev/null
						autossh -M 0 -o "StrictHostKeyChecking no" -R $webapp:80:localhost:65177 -R $oauth:80:localhost:3000 serveo.net 1>/dev/null 2>/dev/null &
                        echo "Restart servizio SERVEO"
                else
                        oauth=`cat /home/pi/server/msh/settings.xml | grep oauth | cut -d\'>\' -f 2 | cut -d\'<\' -f 1`
						webapp=`cat /home/pi/server/msh/settings.xml | grep webapp | cut -d\'>\' -f 2 | cut -d\'<\' -f 1`
                        autossh -M 0 -o "StrictHostKeyChecking no" -R $webapp:80:localhost:65177 -R $oauth:80:localhost:3000 serveo.net 1>/dev/null 2>/dev/null &
                        echo "Avviato servizio SERVEO"
                fi
        ;;
*)      echo "Usage: $0 {start|stop|restart}"
        exit 2
        ;;
esac
exit 0' > serveo.sh
echo "Sposto script serveo.sh in /etc/init.d/serveo"
sudo mv serveo.sh /etc/init.d/serveo
echo "Assegno permessi di esecuzione a /etc/init.d/serveo"
sudo chmod +x /etc/init.d/serveo 1>/dev/null
echo "Eseguo systemctl enable serveo"
sudo systemctl enable serveo 1>/dev/null 2>/dev/null
echo "Eseguo service serveo start"
sudo service serveo start 1>/dev/null
echo "Imposto avvio servizio serveo all'avvio"
sudo update-rc.d serveo enable 1>/dev/null
# SERVIZIO MSH
echo "Creo script msh.sh"
echo $'#!/bin/bash
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
			pgrep python | awk \'{print $0}\' | xargs sudo kill -9 1>/dev/null 2>/dev/null
			echo "Stoppato servizio MSH"
		else
			echo "Servizio MSH non attivo"
		fi
        ;;
restart) if [ $(pgrep python) ]
		 then
			pgrep python | awk \'{print $0}\' | xargs sudo kill -9 1>/dev/null 2>/dev/null
			cd /home/pi/server/msh && sudo python3 msh.py 1>/dev/null 2>/dev/null &
			echo "Restart servizio MSH"
		else
			cd /home/pi/server/msh && sudo python3 msh.py 1>/dev/null 2>/dev/null &
			echo "Avviato servizio MSH"
		fi
        ;;
*)      echo "Usage: $0 {start|stop|restart}"
        exit 2
        ;;
esac
exit 0' > msh.sh
echo "Sposto script msh.sh in /etc/init.d/msh"
sudo mv msh.sh /etc/init.d/msh
echo "Assegno permessi di esecuzione a /etc/init.d/msh"
sudo chmod +x /etc/init.d/msh 1>/dev/null
echo "Eseguo systemctl enable msh"
sudo systemctl enable msh 1>/dev/null 2>/dev/null
echo "Eseguo service msh start"
sudo service msh start 1>/dev/null
echo "Imposto avvio servizio msh all'avvio"
sudo update-rc.d msh enable 1>/dev/null
# TEST
sleep 5
echo "Eseguo test per verificare esito installazione"
if curl -I -X GET http://127.0.0.1:65177/static/page/login.html | grep "200 OK"
then
	echo "INSTALLAZIONE RIUSCITA!!"
else
	echo "INSTALLAZIONE KO!!"
fi
echo "---------------------------------------------------------------------"
echo "Impostare credenziali Account Linking | OAuth | Authorization Code
Client ID: $client_id
Client secret: $client_secret
Authorization URL: https://$OAUTH_DOMAIN.serveo.net/oauth
Token URL: https://$OAUTH_DOMAIN.serveo.net/token"
exit 0
