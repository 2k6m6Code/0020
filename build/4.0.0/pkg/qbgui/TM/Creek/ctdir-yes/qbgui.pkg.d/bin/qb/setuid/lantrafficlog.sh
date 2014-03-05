#!/bin/sh


ip=$1
filename=$2

if [ ! -e /proc/net/ipt_account/$filename ]; then
/sbin/iptables -A FORWARD -m account --aaddr $ip --aname $filename
fi
echo "show=src-or-dst" > /proc/net/ipt_account/$filename

echo "reset" > /proc/net/ipt_account/$filename
sleep 1
echo gettime:`date +"%s"`  >> /usr/local/apache/qb/Log_file/$filename
cat /proc/net/ipt_account/$filename >> /usr/local/apache/qb/Log_file/$filename