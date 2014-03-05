#!/bin/bash

CONFIGVALUE=$1
CONFIGNAME=$2
HACONFPATH=/mnt/qb/conf/ha

unalias cp
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

# if the  HA Conf Path does not exist
if [ -d $HACONFPATH ]; then
    echo ''
else 
    mkdir -p $HACONFPATH
fi

echo $CONFIGVALUE > $HACONFPATH/$CONFIGNAME
sync #20130419 To prevent DOM/CF become readonly
