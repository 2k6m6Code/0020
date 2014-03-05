#!/bin/bash

# Brian 20140124 Kill all tmv devices

echo "Killall TMV devices..."
Alltmvpid=`ps -ef|grep openvpn|awk '{print $2}'|sed 's/\n//g'`
for tmvpid in $Alltmvpid
do
sleep 1
kill -9 $tmvpid
done
    
