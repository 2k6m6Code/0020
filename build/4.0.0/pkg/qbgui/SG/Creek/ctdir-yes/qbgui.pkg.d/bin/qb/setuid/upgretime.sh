#!/bin/bash
set -x
remoteip=$1
time=$2
option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ServerAliveInterval=5 -o ServerAliveCountMax=2 -o ConnectTimeout=5"
ACTIVEBASICXML=/usr/local/apache/active/basic.xml

echo $remoteip >>/tmp/reip
echo $time >>/tmp/reip

#/bin/rm -f /tmp/log

#--------------------------------------------------------------------------
#    Reboot time
#--------------------------------------------------------------------------
if [ "$time" = "24" ];then
    ssh $option $remoteip "reboot"
elif [ "$time" = "0" ];then
    time=24
    ssh $option $remoteip "/opt/qb/bin/script/rebootqb $time"
    time=0 
    ssh $option $remoteip "echo $time >/tmp/reboot_time"
else
    ssh $option $remoteip "/opt/qb/bin/script/rebootqb $time" 
    ssh $option $remoteip "echo $time >/tmp/reboot_time"
fi
