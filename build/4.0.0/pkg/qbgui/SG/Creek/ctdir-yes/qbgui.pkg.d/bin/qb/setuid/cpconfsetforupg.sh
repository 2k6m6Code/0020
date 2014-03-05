#!/bin/bash 

SETNAME=$1
ACTION=$2

PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

UPGPATH=/var/upg
SETPATH=/mnt/qb/conf/set

unalias cp

#==============================================================================================
# if the argument is null string
if [  -z $SETNAME ]; then
    exit 1 
fi

#==============================================================================================
if [ $ACTION = 'to' ]
then
    # if the upgrade path does not exist, make it 
    mkdir -p $UPGPATH
    rm -rf $UPGPATH/$SETNAME
    \cp -rf $SETPATH/$SETNAME $UPGPATH/$SETNAME
    chmod -R 777 $UPGPATH/$SETNAME
#==============================================================================================
elif [ $ACTION = 'back' ]
then
    if [ ! -z $SETNAME ]
    then
        rm -rf $SETPATH/$SETNAME
    fi
    \cp -rf $UPGPATH/$SETNAME  $SETPATH/$SETNAME
    rm -rf $UPGPATH/$SETNAME
#==============================================================================================
elif [ $ACTION = 'delete' ]
then
    if [ ! -z $SETNAME ]
    then
        rm -rf $UPGPATH/$SETNAME
    fi
fi

sync
sync
sync

