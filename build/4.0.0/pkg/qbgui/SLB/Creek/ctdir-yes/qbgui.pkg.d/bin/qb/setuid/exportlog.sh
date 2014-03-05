#!/bin/sh
DIAGNOSE=/var/log/diagnose.log
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

HISPATH=/tmp/qbnethis/new/
NETPATH=/tmp/ispnet/

HOST=$1

USERNAME=$2

PASSWORD=$3

ISPHISLOGNAME=$(date +%s)his.zip
ISPNETLOGNAME=$(date +%s)net.zip

TMPHISLOG=/tmp/$ISPHISLOGNAME
TMPNETLOG=/tmp/$ISPNETLOGNAME
FTPRETRYCOUNT=3


#=================================================
# STEP 1. zip policy history 
#==================================================
# phase 1. zip log files for qbnethis and qbnet rule
# qbnethis:located at => /tmp/qbnethis/new/
# rules:   located at => /tmp/qbnethis/rules
#=================================================
cd $HISPATH
/opt/qb/apps/zip -j $TMPHISLOG  $(find ./* -mtime -1)  ../rules 
ZIPRESULT=$?

if [  ! $ZIPRESULT = 0 ]
then
    echo "ISPHIS: ZIP Process Stopped"
    exit 100
fi

#===============================================
# phase 2. transfer isp history log package to log server
#===============================================
FTPRESULT=1
RETRYCOUNT=$FTPRETRYCOUNT

while [[ $FTPRESULT -ne 0 && $RETRYCOUNT -gt 0 ]]
do 
    ncftpput -S .tmp $HOST -u $USERNAME  -p $PASSWORD . $TMPHISLOG >& /dev/null
    FTPRESULT=$?
    let RETRYCOUNT-=1
done

if [ $FTPRESULT = 0 ]
then
    echo $(date -R) "SUCCESS: exporting isp history log successfully" | tee -a $DIAGNOSE
else
    echo $(date -R) "ERROR: fail to export isp history log" | tee -a $DIAGNOSE
    touch $(find ./*  -mtime -1 )
fi
rm -rf $TMPHISLOG


#=================================================
# STEP 2. zip net traffic log of isp 
#==================================================
# phase 1. zip log files for ispnet
# ispnet:located at => /tmp/ispnet/
#=================================================
cd $NETPATH
/opt/qb/apps/zip -j $TMPNETLOG  $(find ./*  -mtime -1)   
ZIPRESULT=$?

if [  ! $ZIPRESULT = 0 ]
then
    echo "ISPNET: ZIP Process Stopped"
    exit 100
fi

#===============================================
# phase 2. transfer isp net log package to log server
#===============================================
FTPRESULT=1
RETRYCOUNT=$FTPRETRYCOUNT
while [[ $FTPRESULT -ne 0 && $RETRYCOUNT -gt 0 ]]
do
    ncftpput -S .tmp $HOST -u $USERNAME  -p $PASSWORD . $TMPNETLOG >& /dev/null
    FTPRESULT=$?
    let RETRYCOUNT-=1
done

if [  $FTPRESULT = 0 ]
then
    echo $(date -R) "SUCCESS: exporting isp net log successfully" | tee -a $DIAGNOSE
else
    echo $(date -R) "ERROR: fail to export isp net log" | tee -a $DIAGNOSE
    touch $(find ./*  -mtime -1 )
fi
rm -rf $TMPNETLOG
