#!/bin/bash
#set -x
remoteip=$1
localip=$2
action=$3

option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ServerAliveInterval=5 -o ServerAliveCountMax=3 -o ConnectTimeout=5"

if [ "$action" = "1" ];then
    /sbin/wget http://$remoteip:4000/clean/testfile -T 10 -t 1 -o /tmp/speed_file-remote -O /tmp/wgetfile
    /bin/cat /proc/qbalancer/qbreport|grep $remoteip > /tmp/download-$localip
    /bin/rm -f /tmp/wgetfile
    /bin/rm -f /tmp/speed_file-remote
    ssh $remoteip -i /etc/.ssh/qlogin /usr/local/apache/qb/tunnel_speed.sh $remoteip $localip 0 &
    
    if [ -f /tmp/download-$localip ]; then
        /usr/bin/scp -i /etc/.ssh/qlogin $option /tmp/download-$localip $remoteip:/tmp/upload-$remoteip
    fi
elif [ "$action" = "0" ];then
    /sbin/wget http://$localip:4000/clean/testfile -T 10 -t 1 -o /tmp/speed_file-local -O /tmp/wgetfile
    /bin/cat /proc/qbalancer/qbreport|grep $remoteip > /tmp/download-$remoteip
    /bin/rm -f /tmp/wgetfile
    /bin/rm -f /tmp/speed_file-local
    if [ -f /tmp/download-$remoteip ]; then
        /usr/bin/scp -i /etc/.ssh/qlogin $option /tmp/download-$remoteip $localip:/tmp/upload-$localip
    fi
else
    echo 123
    #ssh $option $remoteip "echo $time >/tmp/reboot_time"
fi
