#!/bin/sh
DELIP=$1

#grep -v $DELIP /usr/local/apache/active/userlock_list > /tmp/userlock_list_swap
#cat /tmp/userlock_list_swap > /usr/local/apache/active/userlock_list

#################################################################################
#
# find at rule num to delete it
#
#################################################################################
at_num=`cat /tmp/userlock_list |grep $DELIP |awk '{print $3}'`
`at -d $at_num`


#################################################################################
#
# pick out $DELIP from /tmp/userlock_list
#
#################################################################################
grep -v $DELIP /tmp/userlock_list > /tmp/userlock_list_swap
cat /tmp/userlock_list_swap > /tmp/userlock_list
rm -rf /tmp/userlock_list_swap

#grep -v $DELIP /usr/local/apache/active/userlock_cmd > /tmp/userlock_cmd_swap
#cat /tmp/userlock_cmd_swap > /usr/local/apache/active/userlock_cmd
#grep -v $DELIP /tmp/userlock_cmd > /tmp/userlock_cmd_swap
#cat /tmp/userlock_cmd_swap > /tmp/userlock_cmd
#rm -rf /tmp/userlock_cmd_swap


#################################################################################
#
# Directly delete iptables for $DELIP
#
#################################################################################
/sbin/iptables -D INPUT -s $DELIP -j DROP &
/sbin/iptables -D INPUT -d $DELIP -j DROP &
/sbin/iptables -D FORWARD -s $DELIP -j DROP &
/sbin/iptables -D FORWARD -d $DELIP -j DROP &
/sbin/iptables -D OUTPUT -s $DELIP -j DROP &
/sbin/iptables -D OUTPUT -d $DELIP -j DROP &

echo $DELIP > /tmp/delip

