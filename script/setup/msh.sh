#!/bin/bash
### BEGIN INIT INFO
# Provides:          mio_start_script.sh
# Required-Start:    hal
# Required-Stop:     
# Should-Start:      
# Should-Stop:       
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Attivo servizio MSH
# Description:       Attivo servizio MSH
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
			echo "Stoppato servizio MSH"
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
status) if [ $(pgrep python) ]
		then
			echo "Servizio MSH attivo"
		else
			echo "Servizio MSH non attivo"
		fi
        ;;
*)      echo "Usage: /etc/init.d/msh.sh {start|stop|restart|status}"
        exit 2
        ;;
esac
exit 0