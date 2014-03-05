#!/bin/bash
#set -x
QB_HOME_DIR=/opt/qb
QBREG_FILE=$QB_HOME_DIR/registry
MODEL=$(awk "/MODEL/ {print \$2}"  $QBREG_FILE)

NAME=`cat /mnt/conf/insdate`
STRANGEDEV=$1

echo >>/tmp/maildata
echo "IP Information:" >/tmp/maildata
/sbin/ip addr|grep eth >>/tmp/maildata
/sbin/ip addr|grep mpv >>/tmp/maildata
echo "=====================================" >>/tmp/maildata

echo >>/tmp/maildata
echo "NAT Information:" >>/tmp/maildata
/sbin/iptables -t nat -L -vn|grep 172.31.3.1>>/tmp/maildata
echo "=====================================" >>/tmp/maildata

echo >>/tmp/maildata
echo "User Login Information:" >>/tmp/maildata
cat /mnt/qb/conf/login.xml>>/tmp/maildata
echo "=====================================" >>/tmp/maildata

echo >>/tmp/maildata
echo "User Register Information:" >>/tmp/maildata
cat /mnt/conf/insdate>>/tmp/maildata
echo "=====================================" >>/tmp/maildata

echo >>/tmp/maildata
echo "User Register Time Stamp:" >>/tmp/maildata
rm -f /mnt/conf/dtstamp.dc
mcrypt -d /mnt/conf/dtstamp -k 2k6m6
Seconds=`cat /mnt/conf/dtstamp.dc`
Datetime=`date -d "1970-01-01 UTC $Seconds seconds"`
echo $Datetime>>/tmp/maildata
echo "=====================================" >>/tmp/maildata

echo >>/tmp/maildata
echo "Version Information:" >>/tmp/maildata
cat /mnt/conf/pkginfo|grep "VERSION DETAIL">>/tmp/maildata
echo "=====================================" >>/tmp/maildata

echo >>/tmp/maildata
echo "Serial Number:" >>/tmp/maildata
QBSN=`cat /mnt/conf/qbsn`
echo $QBSN>>/tmp/maildata
echo "=====================================" >>/tmp/maildata

echo >>/tmp/maildata
echo "Contact E-mail:" >>/tmp/maildata
cat /mnt/conf/contact>>/tmp/maildata
echo "=====================================" >>/tmp/maildata

mcrypt /tmp/maildata -k 2k6m6
mv -f /tmp/maildata.nc /tmp/qb.reg

case $STRANGEDEV in
 qbreg )
         /usr/bin/mutt -s "User $NAME's register information in QB $MODEL $QBSN" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         ;; #Register QB
 mpv* )
         /usr/bin/mutt -s "Find a strange link:$STRANGEDEV in User $NAME's QB $MODEL $QBSN" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         ;; #Strange Link
 hck )
         /usr/bin/mutt -s "User $NAME's healthy check information in QB $MODEL $QBSN" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         ;; #Daily information
 noreg )
         /usr/bin/mutt -s "User need to register QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         ;; #Need to register
 vmkey )
         /usr/bin/mutt -s "Fail to get the license key for QB $MODEL $QBSN $VMKEYFAIL_TIMES times" -a /tmp/qb.reg qbreg@creek
.com.tw < /mnt/conf/pkginfo
         ;; #No license key
 vmkey_kill )
         /usr/bin/mutt -s "Fail to get the license key for QB $MODEL $QBSN $VMKEYFAIL_TIMES times and kill this unit" -a /tmp
/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo
         ;; #No license key
 hardware )
         /usr/bin/mutt -s "Hardware error in QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         ;; #Check mac error
 nosn )
         /usr/bin/mutt -s "Get Serial Number Error in QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         ;; #Get Serial number error
 nodate )
         /usr/bin/mutt -s "Get Shipment Date Error in QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         ;; #Get Shipment Date error
 warranty )
         /usr/bin/mutt -s "Warranty expired in QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         MailList=`grep "mail value" /usr/local/apache/qbconf/overview.xml|grep -v system|sed -e "s/.*value=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`
         for mail in $MailList
         do
         /usr/bin/mutt -s "Warranty expired in QB $MODEL" $mail < /mnt/conf/pkginfo &
         done
         ;; #Check warranty error
 license )
         /usr/bin/mutt -s "License will expire in QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /tmp/licensemailinfo &
         MailList=`grep "mail value" /usr/local/apache/qbconf/overview.xml|grep -v system|sed -e "s/.*value=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`
         for mail in $MailList
         do
         /usr/bin/mutt -s "License will expire in QB $MODEL" $mail < /tmp/licensemailinfo &
         done
         ;; #Check license error
 trial )
         /usr/bin/mutt -s "Server will expire in QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /tmp/trialmailinfo &
         MailList=`grep "mail value" /usr/local/apache/qbconf/overview.xml|grep -v system|sed -e "s/.*value=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`
         for mail in $MailList
         do
         /usr/bin/mutt -s "Server will expire in QB $MODEL" $mail < /tmp/trialmailinfo &
         done
         ;; #Check trial error
 * )
         /usr/bin/mutt -s "User $NAME's unknown information in QB $MODEL $QBSN" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo &
         ;; #Unknown 
esac
                                             
#if [ "$STRANGEDEV" = "" ]; then
#   #cat /tmp/maildata|/opt/qb/bin/script/mail -s "User $NAME's register information in QB $MODEL" qbreg@creek.com.tw
#   /usr/bin/mutt -s "User $NAME's register information in QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo
#else
#   #cat /tmp/maildata|/opt/qb/bin/script/mail -s "Find a strange link:$STRANGEDEV in User $NAME's QB $MODEL" qbreg@creek.com.tw
#   /usr/bin/mutt -s "Find a strange link:$STRANGEDEV in User $NAME's QB $MODEL" -a /tmp/qb.reg qbreg@creek.com.tw < /mnt/conf/pkginfo
#fi

rm -f /tmp/qb.reg
rm -f /tmp/maildata
