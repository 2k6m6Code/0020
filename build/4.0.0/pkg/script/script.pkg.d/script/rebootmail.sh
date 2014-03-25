#set -x
if [ -f "/tmp/SHD_failed" -o -f "/tmp/SHD_Crash" ];then
MESSAGE="power cycle"
elif [ -f "/tmp/Please_arrage_reboot" ];then
MESSAGE="reboot"
fi

TYPE=`cat /opt/qb/registry | grep ^TYPE |awk '{print $2}'`
MODE=`cat /opt/qb/registry | grep MODE |awk '{print $2}'`
mailinfo="/tmp/mailinfo"
MailList=`grep "mail value" /usr/local/apache/qbconf/overview.xml|grep -v system|sed -e "s/.*value=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`


#Generate mail text contents
if [ "$MailList" != "" ]
then
    cat >> $mailinfo <<!
Dear User: 

There are some issues occurred with your device $TYPE$MODE. 
Please arrange time to $MESSAGE.

*********************************************************************************************
 Tip: Generated email auto-sent, please do not reply.                             
        If you need help, please feel free to contact our distributor.             
        If this email is regarded as a spam mail, please mark as "not spam".      
*********************************************************************************************

Creek's team.
!
else
 exit 0
fi
                    

#Send mail to all mail accounts
for mail in $MailList
do
   /usr/bin/mutt -s "Please $MESSAGE your $TYPE$MODE " $mail < /tmp/mailinfo & 
done

rm -f $mailinfo
