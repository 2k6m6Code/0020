#! /bin/sh
# ezio setting.
EZIO_PRINT_DEFAULT="/opt/qb/qbwdt/ezio"
EZIO_PRINT="/opt/qb/qbwdt/ezio -c 1 -t "

# basic setting.
DateTime=`/bin/date +%m%d%H%M`
LogDIR="/mnt/log/" 		# "/var/log/"
TarFile="${LogDIR}${DateTime}.tz"

# command list.
Ip1="ip route" 				
Ip2="ip rule"
Iptables1="iptables -t mangle -L -vn"
Iptables2="iptables -t nat -L -vn"
Dmesg="/bin/dmesg -c"
Arp="/sbin/arp -an"
Ifconfig="ifconfig"
Route="ip route show cache" # route.

# copy proc list.
Proc_net_ip="/bin/cp /proc/net/ip_conntrack ${LogDIR}"
## qbconfig  qbdebug  qbdsthash  qbfrag  qbmachash  qbreport  qbtbmap
Proc_qb="/bin/cp /proc/qbalancer/* ${LogDIR}"

# output list.
Ip1_OUT=${LogDIR}ip_route.out
Ip2_OUT=${LogDIR}ip_rule.out
Iptables1_OUT=${LogDIR}iptables_mangle.out
Iptables2_OUT=${LogDIR}iptables_nat.out
Dmesg_OUT=${LogDIR}dmesg.out
Arp_OUT=${LogDIR}arp.out
Ifconfig_OUT=${LogDIR}ifconfig.out
Route_OUT=${LogDIR}route_cache.out
Proc_net_ip_FILE=${LogDIR}ip_conntrack
Proc_qb_FILE="${LogDIR}qb[c-z]*"

# log list.
Qb_LOG="/var/log/qbalancer.log"
Mnt_LOG="/mnt/log/*.log"

# clean mail queue
# rm -rf /var/spool/mqueue/*

# run command.
$Ip1 > $Ip1_OUT
$Ip2 > $Ip2_OUT
$Iptables1 > $Iptables1_OUT
$Iptables2 > $Iptables2_OUT
$Dmesg > $Dmesg_OUT
$Arp > $Arp_OUT
$Ifconfig > $Ifconfig_OUT
$Route > $Route_OUT

$Proc_net_ip
$Proc_qb

# tar log files.
/bin/tar zcf $TarFile \
$Ip1_OUT \
$Ip2_OUT \
$Iptables1_OUT \
$Iptables2_OUT \
$Dmesg_OUT \
$Arp_OUT \
$Ifconfig_OUT \
$Route_OUT \
$Qb_LOG \
$Mnt_LOG \
$Proc_net_ip_FILE \
$Proc_qb_FILE 

/bin/rm -f $Ip1_OUT \
$Ip2_OUT \
$Iptables1_OUT \
$Iptables2_OUT \
$Dmesg_OUT \
$Arp_OUT \
$Ifconfig_OUT \
$Route_OUT \
$Proc_net_ip_FILE \
$Proc_qb_FILE 

# if [ $? -eq 0 ] ; then
if [ -s $TarFile ] ; then
	result="Log:Saved"	
else
	result="Log:Not-Saved"	
fi

# echo ${result}
( $EZIO_PRINT "${result}"; sleep 60; $EZIO_PRINT_DEFAULT) &
