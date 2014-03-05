#!/bin/bash

SOURCE=$1

DIR=$2

XMLPATH=/usr/local/apache/qbconf

ACTIVEPATH=/usr/local/apache/active

DIAGNOSE=/var/log/diagnose.log

if [ -n "$DIR"  ] ; then 
    SETPATH=/mnt/qb/conf/cms/$DIR/
else
    SETPATH=/mnt/qb/conf/set/
fi
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin

export PATH

unalias cp

#=====================================================
# read version number of now using xml format
NOWXMLVERSION=$(cat /usr/local/apache/qb/XMLVERSION)

#==============================================================================================
# if the argument is null string
if [  -z $SOURCE ]; then
	echo "Please Give the name of the Config. Set"
        exit 1 
fi

#==============================================================================================
# if the Config Set Path of DOM does not exist, make it 
mkdir -p $SETPATH

if [ $SOURCE = "active" ]; then
    SOURCEPATH=$ACTIVEPATH
else 
    SOURCEPATH=$SETPATH/$SOURCE
fi  
  
#=====================================================
# read version number of source xml format 
# Possible in :
# 1. xmlver
# 2. version
# 3. none
SRCXMLVERSION=$(cat $SOURCEPATH/xmlver)
if [[ -z $SRCXMLVERSION ]] 
then
    SRCXMLVERSION=$(cat $SOURCEPATH/version)
    if [[ -z $SRCXMLVERSION ]] 
    then
        if [[ -f $SOURCEPATH/lvsnet.xml ]]
        then
            SRCXMLVERSION='2.2.0.0000'
        else
            SRCXMLVERSION='2.1.5.0000'
        fi
    fi
fi

#==============================================================================================
# if version  of this xml set can not be used , report it and ask user to upgrade this config !!
if [[ $NOWXMLVERSION != $SRCXMLVERSION ]] 
then
    echo "1. Config. version does not match" | tee -a $DIAGNOSE
    echo "2. $NOWXMLVERSION is needed, but $SOURCE is of version $SRCXMLVERSION "
    echo "3. An upgrade process is needed for Config. set $SOURCE "
    exit 1
fi


#==============================================================================================
# if the Config Path does not exist, make it 
mkdir -p $XMLPATH

#==============================================================================================
# if the Active Config Path does not exist, make it 
mkdir -p $ACTIVEPATH


if [ -f $SOURCEPATH/basic.xml ]; then
    echo ""
else
    echo $(date) "Config. Set $SOURCE NOT exists" | tee -a $DIAGNOSE
    exit 1
fi

cp -rf $SOURCEPATH/*  $XMLPATH/
copy_status=$?

if [[ ${copy_status} != '0' ]]
then
    echo $(date) "ERROR: Fail to LOAD Config. $SOURCE"  | tee -a $DIAGNOSE
    exit ${copy_status}
else
    chmod -R 777 $XMLPATH
    echo $(date) "Config. Set $SOURCE Loaded Successfully" | tee -a $DIAGNOSE
    sync
fi
