#! /bin/sh
#set -x
CMD=$1
ARGV=$2
ispid=$3
devname=$4
ispname=$5

SNMPTRAP=/opt/snmpd/snmptrap

SNMPCONF_FILE=/mnt/conf/snmpd.con

if [ -f $SNMPCONF_FILE ]; then
	SNMPTRAP=$(awk '/#snmptrap/{print $2}' $SNMPCONF_FILE )
	MANAGER=$(awk '/#manager /{print $2}' $SNMPCONF_FILE )
	MANAGER_2=$(awk '/#manager2/{print $2}' $SNMPCONF_FILE )
	COMMUNITY=$(awk '/rocommunity/{print $2}' $SNMPCONF_FILE )
else
	SNMPTRAP=disable
fi

if [ "$SNMPTRAP" = "enable" ]; then
	#echo "snmptrap will send $CMD message  "
	echo "snmptrap will send $CMD message with ISP$3 $4 $5 "
else
	exit 0 
fi

if [ "$CMD" = "coldstart" ]; then 
	/opt/snmpd/snmptrap -v 1 -c $COMMUNITY $MANAGER "" "" 0 0 ""
	/opt/snmpd/snmptrap -v 1 -c $COMMUNITY $MANAGER_2 "" "" 0 0 ""
fi

if [ "$CMD" = "linkup" ]; then 
	#/opt/snmpd/snmptrap -v 1 -c public $MANAGER enterprises.spider test-hub 3 0 '' \
	#interfaces.iftable.ifentry.ifindex.$ARGV i 1
        /opt/snmpd/snmptrap -v 1 -c $COMMUNITY $MANAGER .1.3.6.1.4.1.28116.20 $MANAGER 3 5247 "" 1.3.6.1.4.1.28116.20.1 s "ISP$ispid $devname $ispname Linkup Trap"
        /opt/snmpd/snmptrap -v 1 -c $COMMUNITY $MANAGER_2 .1.3.6.1.4.1.28116.20 $MANAGER_2 3 5247 "" 1.3.6.1.4.1.28116.20.1 s "ISP$ispid $devname $ispname Linkup Trap"
fi

if [ "$CMD" = "linkdown" ]; then 
	#/opt/snmpd/snmptrap -v 1 -c public $MANAGER "" "" 0 0 ""
        #/opt/snmpd/snmptrap -v 1 -c public $MANAGER .1.3.6.1.4.1.28116.20 $MANAGER 2 5247 "" 1.3.6.1.4.1.28116.20.1 s "ISP $ARGV Linkdown Trap"
        /opt/snmpd/snmptrap -v 1 -c $COMMUNITY $MANAGER .1.3.6.1.4.1.28116.20 $MANAGER 2 5247 "" 1.3.6.1.4.1.28116.20.1 s "ISP$ispid $devname $ispname Linkdown Trap"
        /opt/snmpd/snmptrap -v 1 -c $COMMUNITY $MANAGER_2 .1.3.6.1.4.1.28116.20 $MANAGER_2 2 5247 "" 1.3.6.1.4.1.28116.20.1 s "ISP$ispid $devname $ispname Linkdown Trap"
fi
