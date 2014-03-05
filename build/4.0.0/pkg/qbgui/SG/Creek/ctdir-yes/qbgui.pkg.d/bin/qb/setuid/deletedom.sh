#!/bin/bash

DELETE=$1

SETPATH=/mnt/qb/conf/set
DIAGNOSE=/var/log/diagnose.log

unalias cp
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

# if the argument is null string
if [  -z $DELETE ]; then
	echo "Give the name of the Config. Set"
        exit 1 
fi

# if the Config does exist delete it, or report Warnning
if [  -d $SETPATH/$DELETE ]; then

    rm -rf $SETPATH/$DELETE
    rm_status=$?
    
    if [[ ${rm_status} != '0' ]];  then
        echo $(date) "ERROR: Fail to Delete Config. Set $DELETE"  | tee -a $DIAGNOSE
        exit ${rm_status}
    else
        echo $(date) "Config. Set $DELETE Deleted Successfully" | tee -a $DIAGNOSE
        sync
    fi

else
    echo $(date) "Config. Set $DELETE NOT exists" | tee -a $DIAGNOSE
    exit 1

fi

