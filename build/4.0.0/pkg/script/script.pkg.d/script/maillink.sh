#set -x
ispid=$1
ispname=$2
systemip=$3
gateway=$4
device=$5
mailinfo="/tmp/mailinfo"
MailList=`grep "mail value" /usr/local/apache/qbconf/overview.xml|grep -v system|sed -e "s/.*value=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`

#Generate mail text contents
if [ "$MailList" != "" ]
then
    cat >> $mailinfo <<!
Line reestablished: 
ISP #$ispid ($ispname) with gateway address $gateway and system ip address $systemip has recovered on port $device.

 Note: If you have received many such notices in a short period of time, it may indicate two conditions:
 1. The parameters given for the line condition check result in over-sensitivity and are prone to produce false alarms.
 2. The line connection is instable.
!
else
 exit 0
fi
                    

#Send mail to all mail accounts
for mail in $MailList
do
   /usr/bin/mutt -s "Qbalancer Link Status Notification:ISP #$ispid ($ispname) " $mail < /tmp/mailinfo & 
done

rm -f $mailinfo
