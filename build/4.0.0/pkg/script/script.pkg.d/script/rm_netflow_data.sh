#!/bin/sh
#set -x

#
# keep 5 days data
# delete 6 days ago of data
#

LOGADDR="/mnt/tclog/nfcapd."
KEEPDATA=5
DELDATACOUNT=2

for (( i=$KEEPDATA ; i<`expr $KEEPDATA + $DELDATACOUNT` ; i = i + 1 ))
do
/bin/rm -rf $LOGADDR`date "+%Y%m%d" -d'-'$i' day'`*
done

