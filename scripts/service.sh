#! /bin/bash
### BEGIN INIT INFO
# Provides:          ckan
# Required-Start:    $local_fs
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# X-Interactive:     false
# Short-Description: Ckan init script
# Description:       Start/stop script
### END INIT INFO

echo "Sevice CKAN!"

PATH=/usr/lib/ckan/default/bin:$PATH


NAME=ckan
RUNAS=user
DESC="CKAN Service Launcher"


CKAN_DIR="/usr/lib/ckan/default/src/ckan/"
CKAN_INI="/etc/ckan/default/development.ini"
CKAN_LOG="/home/user/ckan.log"
CKAN_PID="/home/user/ckan.pid"

set -e


do_start () {
   echo "Starting ckan..."
   cd $CKAN_DIR
   nohup paster serve $CKAN_INI > $CKAN_LOG 2>&1 & echo $! > $CKAN_PID
   echo "Started"
}

do_stop () {
   echo "Stoping ckan..."
   kill -9 $(cat $CKAN_PID)
	echo "Stopped"
}

do_status () {
   PROCESS_GREP=$(ps -aux | grep $(cat $CKAN_PID) | grep -v grep)
   if [[ $PROCESS_GREP == "" ]];
   then
       echo "Running. PID: $(cat $CKAN_PID)"
   else
       echo "Not running"
   fi
}


do_restart() {
   echo "Restarting..."
}

case "$1" in
 start)
	do_start
	;;
 stop)
	do_stop
	;;
 status)
 	do_status
 	;;
 *)
	echo "Usage: $0 start|stop|status" >&2
	exit 3
	;;
esac

exit 0
