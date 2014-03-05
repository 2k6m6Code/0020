#! /bin/sh

EZIO_PRINT_DEFAULT="/opt/qb/qbwdt/ezio"
EZIO_PRINT="/opt/qb/qbwdt/ezio -c 1 -t "

# clean mail queue
# rm -rf /var/spool/mqueue/*

# run command.
killall -9 qbcli
## /opt/qb/console/qbcli remote ### ??

result="qbcli:Restart"

( $EZIO_PRINT $result; sleep 60; $EZIO_PRINT_DEFAULT) &

