#!/bin/bash
#set -x

TYPE=$1
ATT=$2
UP_FILE="/mnt/qb/conf/auth"
PAGE_DIR="/usr/local/apache/qb/auth/"

if [ $TYPE == 'logo' ]
then
    TMP_UPLOAD_FILE="/tmp/tmpupg/logo.png"
    UPLOAD_FILE="/mnt/qb/conf/auth/image"
    FILE="logo.png"
fi

if [ $TYPE == 'm_att' ]
then
    TMP_UPLOAD_FILE="/tmp/tmpupg/message.tmp"
    UPLOAD_FILE="/mnt/qb/conf/auth/$ATT"
    FILE="message.tmp"
fi

#============P1==============
if [ ! -e $UP_FILE ]
then
    mkdir $UP_FILE
fi

if [ ! -e $UPLOAD_FILE ]
then
    mkdir $UPLOAD_FILE
fi

rm -rf $UPLOAD_FILE/*

chmod 777 $TMP_UPLOAD_FILE

cp $TMP_UPLOAD_FILE $UPLOAD_FILE

cp $TMP_UPLOAD_FILE $PAGE_DIR

sync
sync
sync
