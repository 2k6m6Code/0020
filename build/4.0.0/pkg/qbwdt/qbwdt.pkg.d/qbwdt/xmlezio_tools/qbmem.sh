#! /bin/sh

EZIO_PRINT_DEFAULT="/opt/qb/qbwdt/ezio"
EZIO_PRINT="/opt/qb/qbwdt/ezio -c 1 -t "

# clean mail queue
# rm -rf /var/spool/mqueue/*

# run command.
memsize=$(cat /proc/meminfo| awk '/MemFree/ {print $2}')
( $EZIO_PRINT "Memory Free:[ ${memsize} KB ]"; sleep 60; $EZIO_PRINT_DEFAULT) &

