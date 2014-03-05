#!/bin/sh
#
# To extract an UPG file to a new created sub-directory with the same
# UPG name.
#
#set -x
if [ $# -ne 1 ]; then
	echo "Usage : $0 <upg-file>"
	exit 1
fi

UPG_FILE=$1

FILE_NAME=`basename $UPG_FILE`
LEN=`echo $FILE_NAME | wc -c | awk '{print $1}'`
P1=`expr $LEN - 5`
P2=`expr $LEN - 3`
P3=`expr $LEN - 1`
UPG_NAME=`echo $FILE_NAME | cut -c1-${P1}`
EXT_NAME=`echo $FILE_NAME | cut -c${P2}-${P3}`

if [ ! "x$EXT_NAME" = "xupg" ]; then
	echo "Error ! file extension has to be .upg !"
	exit 1
fi

DESCRYPTED_FILE=$UPG_FILE.dc

rm -f $DESCRYPTED_FILE

rm -rf $UPG_NAME; mkdir $UPG_NAME

mcrypt $UPG_FILE -d -k 42084021

(cd $UPG_NAME; tar xfz ../$DESCRYPTED_FILE)
rm -f $DESCRYPTED_FILE

