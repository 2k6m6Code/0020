#!/bin/bash
option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ServerAliveInterval=30 -o ServerAliveCountMax=10 -o ConnectTimeout=30"
remoteip=$1
#create folder save log
/bin/rm -f /tmp/$remoteip/log
mkdir /tmp/$remoteip
#start upload Image to client
scp $option /tmp/PKG1/*.pkg $remoteip:/tmp/tmpupg/image.tmp
#start updata   
ssh $option $remoteip "/usr/local/apache/qb/setuid/qbimg.sh" >>/tmp/$remoteip/log
#start upload Image to client
scp $option /tmp/PKG2/*.pkg $remoteip:/tmp/tmpupg/image.tmp
#start updata   
ssh $option $remoteip "/usr/local/apache/qb/setuid/qbimg.sh" >>/tmp/$remoteip/log