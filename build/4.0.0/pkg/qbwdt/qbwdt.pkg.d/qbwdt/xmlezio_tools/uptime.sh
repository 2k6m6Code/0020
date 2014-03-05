#! /bin/sh

EZIO_PRINT_DEFAULT="/opt/qb/qbwdt/ezio"
EZIO_PRINT="/opt/qb/qbwdt/ezio -c 1 -t "

# clean mail queue
# rm -rf /var/spool/mqueue/*

arg=$1

# run command.
if [ "$arg" = "time" ] ;then
	uptime=$(uptime|awk -F"up" '{print $2}'|awk -F"user" '{print $1}'|awk -F"," 'NF==3 {print $1","$2}; NF==2 {print $1}'|tr -d " "|sed 's/:/hrs/')
	( $EZIO_PRINT "Running Time:${uptime}"; sleep 60; $EZIO_PRINT_DEFAULT) &
else # load average
	uptime=$(uptime|awk -F"load average:" '{print $2}'|tr -d " ")
	( $EZIO_PRINT "Load Average:${uptime}"; sleep 60; $EZIO_PRINT_DEFAULT) &
fi

