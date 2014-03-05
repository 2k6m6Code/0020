#set -x

nic=$1
action=$2
update=$3

/sbin/ip link set $nic $action


if [ $update = '1' ]; then
/bin/echo '100000000000' >/tmp/fifo.qbserv &
sleep 1
/bin/echo '100000000000' >/tmp/fifo.qbserv &
fi
