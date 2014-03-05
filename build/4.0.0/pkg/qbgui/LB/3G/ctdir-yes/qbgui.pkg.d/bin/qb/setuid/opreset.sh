#!/bin/sh
ip=$1
name=$2
if [ ! -e /proc/net/ipt_account/$name ]; then
iptables -A FORWARD -m account --aaddr $ip --aname $name
fi
echo "show=src-or-dst" > /proc/net/ipt_account/$name
echo "reset" > /proc/net/ipt_account/$name
