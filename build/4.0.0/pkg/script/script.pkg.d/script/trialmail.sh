#set -x
AfterDays=$1
version=`cat /mnt/conf/pkginfo | grep "VERSION DETAIL" | awk '{print $4}'|sed s/,//g`
model=`cat /opt/qb/registry|grep "MODEL"|awk '{print $2}'|sed s/,//g`

trialmailinfo="touch /tmp/trialmailinfo"
trialmail="/tmp/trialmailinfo"
MailList=`grep "mail value" /usr/local/apache/qbconf/overview.xml|grep -v system|sed -e "s/.*value=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`
QBSN=`cat /mnt/conf/qbsn`
#Generate mail text contents
if [ "$MailList" != "" ]
then
    cat >> $trialmail <<!
Dear Q-Balancer User,

The Warranty of Q-Balancer- $QBSN will expire after $AfterDays days.
Please contact the distributor/supplier to extend the warranty as soon as you can.

!
else
 exit 0
fi
                    

#Send mail to all mail accounts
for mail in $MailList
do
   /usr/bin/mutt -s "The Warranty Expiry of Q-Balancer- $QBSN will expire after $AfterDays days." $mail < /tmp/trialmailinfo & 
done
rm -f $trialmailinfo
