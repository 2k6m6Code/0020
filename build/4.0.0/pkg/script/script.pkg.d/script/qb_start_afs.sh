#! /bin/sh
EZIO_PRINT="/opt/qb/qbwdt/ezio -c 1 -t "
QBREG_FILE="/opt/qb/conf/registry"
MODEL=$(awk  "/MODEL/  { print \$2 }" $QBREG_FILE)
ENGINE=$(awk  "/ENGINE/ { print \$2 }" $QBREG_FILE)

if [[ -n $ENGINE ]]  # for odm...050128
then
        $EZIO_PRINT "$ENGINE:status[active]"
else
	$EZIO_PRINT "Q-Balancer $MODEL:status[active]"
fi

