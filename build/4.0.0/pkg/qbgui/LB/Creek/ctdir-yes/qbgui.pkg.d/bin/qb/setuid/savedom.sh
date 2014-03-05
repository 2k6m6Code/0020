#!/bin/bash

TARGET=$1
MAXCONFIGID=5
BOOTCONFIGID=boot
XMLPATH=/usr/local/apache/qbconf
ACTIVEPATH=/usr/local/apache/active
INITPATH=/usr/local/apache/config
DIAGNOSE=/var/log/diagnose.log

CONFPATH=/mnt/qb/conf
SETPATH=/mnt/qb/conf/set
HACONFPATH=/mnt/qb/conf/ha

unalias cp
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/opt/qb/sbin:/opt/qb/bin
export PATH

# if the argument is null string
if [ -z $TARGET ]; then
    echo "Please Give a Config Name"
    exit 1 
fi

if [ $TARGET = "active" ]; then
    mkdir -p $ACTIVEPATH
    TARGETPATH=$ACTIVEPATH
else
    mkdir -p $SETPATH
    TARGETPATH=$SETPATH/$TARGET
fi    
    
mkdir -p $TARGETPATH

cp -rf $XMLPATH/*  $TARGETPATH/
copy_status=$?

chmod -R 777 $TARGETPATH                       

if [[ ${copy_status} != '0' ]]
then
    echo $(date) "ERROR: Fail to Save Config." | tee -a $DIAGNOSE
    exit ${copy_status}
else
    echo $(date) "Config. Set $TARGET Saved Successfully." | tee -a $DIAGNOSE
    cp -f $INITPATH/*  $CONFPATH/
    sync
fi
#..........................................................
# 2008-1226 Brian
# Export config file to ftp server.
#..........................................................
ACTIVEBASICXML=/usr/local/apache/active/overview.xml
enablecfgftpserver=`grep enablecfgftpserver $ACTIVEBASICXML|sed -e "s/<opt.*enablecfgftpserver=\"//"|sed -e "s/\".*//"`
ftpmode=`grep ftpmode $ACTIVEBASICXML|sed -e "s/<opt.*ftpmode=\"//"|sed -e "s/\".*//"`
cfgftpserver=`grep cfgftpserverip $ACTIVEBASICXML|sed -e "s/<opt.*cfgftpserverip=\"//"|sed -e "s/\".*//"`
cfgftpusername=`grep cfgftpserverip $ACTIVEBASICXML|sed -e "s/<opt.*cfgftpusername=\"//"|sed -e "s/\".*//"`
cfgftppassword=`grep cfgftpserverip $ACTIVEBASICXML|sed -e "s/<opt.*cfgftppassword=\"//"|sed -e "s/\".*//"`
cfgftpdirectory=`grep cfgftpdirectory $ACTIVEBASICXML|sed -e "s/<opt.*cfgftpdirectory=\"//"|sed -e "s/\".*//"`
if [ $enablecfgftpserver ] && [ $cfgftpserver ] && [ $TARGET != "active" ]
then

case "$cfgftpserver" in
*[0-9]*\.*[0-9]*\.*[0-9]*\.*[0-9]*)
 ping $cfgftpserver -c 2 >/dev/null
 testresult=$?
 if [ "$testresult" = "1" ]; then
 echo "\n"
 echo "No route to ftp server : $cfgftpserver"
 exit 1
 fi
 HOST=$cfgftpserver
;;
*)
 cfgftpserverip=`/opt/qb/bin/script/ns $cfgftpserver`
 if [ "$cfgftpserverip" = "" ]; then
 echo "\n"
 echo "Fail to resolve the ftp server : $cfgftpserver"
 exit 1
 fi
 ping $cfgftpserverip -c 2 >/dev/null
 testresult=$?
 if [ "$testresult" = "1" ]; then
 echo "\n"
 echo "No route to ftp server : $cfgftpserver($cfgftpserverip)"
 exit 1
 fi
 HOST=$cfgftpserverip
;;
esac
    echo "\n"
    /usr/local/apache/qb/setuid/export.sh $TARGET $TARGET.cfg
    echo "\n"
    echo "Connect to FTP server...." | tee -a $DIAGNOSE
#HOST=$cfgftpserver
USER=$cfgftpusername
PASSWD=$cfgftppassword
DIR=$cfgftpdirectory
FILE=$TARGET.cfg
cd /tmp/bak/
if [ $DIR != '' ] && [ "$ftpmode" = "1" ]
then
ftp -inv $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
passive
mkdir $DIR
cd $DIR
binary
put $FILE
reset
bye
END_SCRIPT
elif [ $DIR != '' ] && [ "$ftpmode" = "0" ];then
ftp -inv $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
mkdir $DIR
cd $DIR
binary
put $FILE
reset
bye
END_SCRIPT
elif [ $DIR = '' ] && [ "$ftpmode" = "1" ];then
ftp -inv $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
passive
binary
put $FILE
reset
bye
END_SCRIPT
else
ftp -inv $HOST <<END_SCRIPT
quote USER $USER
quote PASS $PASSWD
binary
put $FILE
reset
bye
END_SCRIPT
fi
rm -rf /tmp/bak
exit 0

fi
