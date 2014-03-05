#set -x
AfterDays=$1
model=`cat /opt/qb/registry|grep "MODEL"|awk '{print $2}'|sed s/,//g`
licensemailinfo="/tmp/licensemailinfo"
MailList=`grep "mail value" /usr/local/apache/qbconf/overview.xml|grep -v system|sed -e "s/.*value=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`
Expired=`cat /tmp/licenseserial |awk '{print $2}'|sed s/,//g`
License_Expired=`date -d "$Expired"`
QBSN=`cat /mnt/conf/qbsn`


#Generate mail text contents
if [ "$MailList" != "" ]
then
    cat >> $licensemailinfo <<!
Dear Q-Balancer User,

The License of virtual Q-Balancer- $QBSN will expire on $Expired after $AfterDays days.
Please contact the distributor/supplier to extend the license as soon as you can.

!
else
 exit 0
fi
                    

#Send mail to all mail accounts
for mail in $MailList
do
   /usr/bin/mutt -s "The License of virtual Q-Balancer- $QBSN will expire on $Expired" $mail < /tmp/licensemailinfo & 
done
rm -f $licensemailinfo
