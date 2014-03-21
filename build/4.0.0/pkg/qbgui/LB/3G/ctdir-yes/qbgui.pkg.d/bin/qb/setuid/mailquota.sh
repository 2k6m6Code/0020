#set -x
name=$1
quota=$2
type=$3
src=$4
dest=$5
qn=$6

mailinfo="/tmp/mailinfo"
MailList=`grep "mail value" /usr/local/apache/qbconf/overview.xml|grep -v system|sed -e "s/.*value=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`

if [ "$type" == "ip" ];
then
	UserMailList=`grep "$name" /usr/local/apache/qbconf/auth.xml|grep -v system|sed -e "s/.*mail=\"//"|sed -e "s/\".*//"|sed 's/\n//g'`
fi


if [ "$type" == "policy" ];
then
	cat >> $mailinfo <<!
Policy Routing Quota Bandwith is $quota
Source:	$src
Destination: $dest

If you want to restore it.
You need to reset quota or delete quota policy from Status -> Quota.
!
elif [ "$type" == "port" ];
then
	cat >> $mailinfo <<!
Link Quota $name
Quota Bandwith is $quota

If you want to restore it.
You need to reset quota or delete quota policy from Status -> Quota.
!
elif [ "$type" == "ip" ];
then
	cat >> $mailinfo <<!
Authentication Quota $name
Quota Bandwith is $quota

If you want to restore it.
You need to reset quota or delete quota policy from Status -> Quota.
!

#else
#	exit 0
fi

#Generate mail text contents
if [ "$MailList" != "" ];
then
#if [ "$type" == "policy" ]
#then
	cat $mailinfo
#else
#	exit 0
fi

#Send mail to all mail accounts
if [ $qn == "1" ];
then
for mail in $MailList
do
	if [ "$type" == "policy" ];
	then
	/usr/bin/mutt -s "Qbalancer Quota Status Notification: #$src -> $dest " $mail < /tmp/mailinfo & 
	else
	/usr/bin/mutt -s "Qbalancer Quota Status Notification: #$name " $mail < /tmp/mailinfo & 
	fi
done
elif [ $qn == "2" ]
then
for mail in $UserMailList
do
	/usr/bin/mutt -s "Qbalancer Quota Status Notification: #$name " $mail < /tmp/mailinfo & 
done
elif [ $qn == "3" ]
then
for mail in $MailList
do
	/usr/bin/mutt -s "Qbalancer Quota Status Notification: #$name " $mail < /tmp/mailinfo & 
done
for mailuser in $UserMailList
do
	#/usr/bin/mutt -s "Qbalancer Quota Status Notification: #$name " $mailuser < /tmp/mailinfo
	/usr/bin/mutt -s "Qbalancer Quota Status Notification: #asdf " jianyu@creek.com.tw < /tmp/quota
done
fi

rm -f $mailinfo
