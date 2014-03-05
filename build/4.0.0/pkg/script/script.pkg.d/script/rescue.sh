#! /bin/sh
R_LEVEL=$1

RUNWAYLOG=/mnt/log/runway.log
EZIO_PRINT="/opt/qb/qbwdt/ezio -c 1 -t "

if [[ $R_LEVEL = "1" ]];
then
	echo $(date -R) "rescure.sh is called : RESCUE LEVEL 1" | tee -a $RUNWAYLOG
        $EZIO_PRINT "Warnning:rescure.sh"

	/usr/local/sbin/ip route flush cache	

	MAX_SIZE=$(cat /proc/sys/net/ipv4/route/max_size)

	let NEW_SIZE=$MAX_SIZE*2

	echo $NEW_SIZE > /proc/sys/net/ipv4/route/max_size
fi



