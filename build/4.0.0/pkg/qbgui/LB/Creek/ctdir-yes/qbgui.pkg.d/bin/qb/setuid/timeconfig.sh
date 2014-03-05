#! /bin/bash

zonename=$1
DIAGNOSE=/var/log/diagnose.log

unalias cp
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

echo $(date) "Try to Set Timezone to $zonename" | tee -a  $DIAGNOSE

# if the argument is null string
if [  -z $zonename ]; then
	echo $(date) "ERROR: Invalid zone name $zonename" | tee -a $DIAGNOSE
        exit 1 
fi

#20130522 Brian Another method to change the timezone
#sed -i -e "s#ZONE=.*#ZONE=$zonename#" /etc/sysconfig/clock
#cp -f /usr/share/zoneinfo/$zonename /etc/localtime

timeconfig $zonename
set_time_config_status=$?

if [[ ${set_time_config_status} != '0' ]]
then
    echo $(date) "ERROR: Fail to Set Timezone as $zonename" | tee -a $DIAGNOSE
    exit ${set_time_config_status}
else
    cp -f /etc/localtime /mnt/conf/loc_time

    echo $(date) "Set Timezone to $zonename Successfully" | tee -a $DIAGNOSE
    
fi

sync
sync
sync
