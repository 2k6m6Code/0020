#set -x 

targetip=$1
limit_time=$2
# get time after 30 min
#end_time=`date "+%Y%m%d%H%M" -d'-'$limit_time' min'`

################################################################################3
#
# end_time
#
################################################################################3
end_time=`date -d $limit_time' min'`   

################################################################################3
#
# end time minute(min) converted to seconds(s)
#
################################################################################3
end_time=`date --date="$end_time" +%s`

#echo $targetip > /usr/local/apache/active/garytest

#grep $targetip /usr/local/apache/active/userlock_list

# if goto is true, do nothing
grep $targetip /tmp/userlock_list
goto=$?

################################################################################3
#
# write some del iptable rule in /tmp/$targetip
# let 'at' schedule command to use.
#
################################################################################3
echo	"/sbin/iptables -D INPUT -s $targetip -j DROP & \
/sbin/iptables -D INPUT -d $targetip -j DROP & \
/sbin/iptables -D FORWARD -s $targetip -j DROP & \
/sbin/iptables -D FORWARD -d $targetip -j DROP & \
/sbin/iptables -D OUTPUT -s $targetip -j DROP &	\
/sbin/iptables -D OUTPUT -d $targetip -j DROP &	\
grep -v $targetip /tmp/userlock_list > /tmp/userlock_list_swap ;\
cat /tmp/userlock_list_swap > /tmp/userlock_list ;\
rm -rf /tmp/userlock_list_swap " > /tmp/$targetip 

################################################################################3
#
# run 'at' schedule command 
# if time is end time
# 'at' schedule command will run predefined rules to del iptables rules
#
################################################################################3
at -f /tmp/$targetip now + 30 minutes >/dev/null 2>&1
at_num=`at -l | awk '{print $1}'|sort -nr |head -1`

################################################################################3
#
# Build /tmp/userlock_list file
# They are all black list IPs
# and setup iptables to block it.
#
################################################################################3
#if [ ! -e "/usr/local/apache/active/userlock_list" ];then
if [ ! -e "/tmp/userlock_list" ];then
	#echo $targetip > /usr/local/apache/active/userlock_list
	echo "$targetip $end_time $at_num" > /tmp/userlock_list
	/sbin/iptables -D INPUT -s $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I INPUT -s $targetip -j DROP &
	/sbin/iptables -D INPUT -d $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I INPUT -d $targetip -j DROP &
	/sbin/iptables -D FORWARD -s $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I FORWARD -s $targetip -j DROP &
	/sbin/iptables -D FORWARD -d $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I FORWARD -d $targetip -j DROP &
	/sbin/iptables -D OUTPUT -s $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I OUTPUT -s $targetip -j DROP &
	/sbin/iptables -D OUTPUT -d $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I OUTPUT -d $targetip -j DROP &
elif [ "$goto" -eq "1" ];then
	#echo $targetip >> /usr/local/apache/active/userlock_list
	echo "$targetip $end_time $at_num" >> /tmp/userlock_list

	/sbin/iptables -D INPUT -s $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I INPUT -s $targetip -j DROP &
	/sbin/iptables -D INPUT -d $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I INPUT -d $targetip -j DROP &
	/sbin/iptables -D FORWARD -s $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I FORWARD -s $targetip -j DROP &
	/sbin/iptables -D FORWARD -d $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I FORWARD -d $targetip -j DROP &
	/sbin/iptables -D OUTPUT -s $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I OUTPUT -s $targetip -j DROP &
	/sbin/iptables -D OUTPUT -d $targetip -j DROP >/dev/null 2>&1 &
	/sbin/iptables -I OUTPUT -d $targetip -j DROP &

fi

################################################################################3
#
# delete /tmp/$targetip 
#
################################################################################3
rm -f /tmp/$targetip
 

