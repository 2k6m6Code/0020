#set -x

alias_IP=$1
nic=$2
action=$3

#/sbin/ip address add $alias_subnet broadcast \+ dev $nic label $alias_nic
/sbin/ip a $action $alias_IP dev $nic

sync

