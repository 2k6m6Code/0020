#!/bin/bash
#set -x
ip=$1
#option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ConnectTimeout=3"
option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ServerAliveInterval=3 -o ServerAliveCountMax=2 -o ConnectTimeout=3"
scp $option /usr/local/apache/qb/setuid/getallinfo.sh $ip:/tmp/
info=`ssh $option $ip "/tmp/getallinfo.sh"`
echo $info
