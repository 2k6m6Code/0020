#!/bin/sh
QB_HOME_DIR=/opt/qb
QBREG_FILE=$QB_HOME_DIR/registry
M_TYPE="MODEL"

MINMODEL=1000 #1610
MODEL=$(awk "/$M_TYPE/ { print \$2 }" $QBREG_FILE|head -n 1)
KERNEL_PARAMS_PREFIX=net.ipv4.netfilter

#######
# old
# [ ! -z $MODEL ] && [ $MODEL != "S400" -a $MODEL -ge $MINMODEL ] && /sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_max=102400

#[ ! -z $MODEL ] && [ $MODEL != "S400" -a $MODEL != "S400Lite" -a $MODEL -ge $MINMODEL ] && Ip_Conntrack_Max=102400

if [ ! -z $MODEL ] 
then
    case $MODEL in
        8?? )  Ip_Conntrack_Max=25600 ;;   # ex. 800
        S2?? )  Ip_Conntrack_Max=20480 ;;   # ex. S200
        S2?* )  Ip_Conntrack_Max=10240 ;;   # ex. S200
        S4?? )  Ip_Conntrack_Max=51200 ;;   # ex. S400
        S4?* )  Ip_Conntrack_Max=10240 ;;   # ex. S400Lite
        25  )  Ip_Conntrack_Max=30000 ;;   # ex. SG 25 
        50  )  Ip_Conntrack_Max=50000 ;;   # ex. SG 50 
        60  )  Ip_Conntrack_Max=50000 ;;   # ex. SG 60 
        100  )  Ip_Conntrack_Max=80000 ;;   # ex. SG 100
        150  )  Ip_Conntrack_Max=100000 ;;   # ex. SG 150
        250  )  Ip_Conntrack_Max=300000 ;;   # ex. SG 250
        500  )  Ip_Conntrack_Max=500000 ;;   # ex. SG/SLB 500
        602* )  Ip_Conntrack_Max=50000 ;;   # ex. LB 602/602D
        1000 )  Ip_Conntrack_Max=1000000 ;;   # ex. SG 1000
        1010 )  Ip_Conntrack_Max=1024000 ;;  # ex. SG 1010 
        2000 )  Ip_Conntrack_Max=1024000 ;;  # ex. SG 2000 
        520  )  Ip_Conntrack_Max=51200 ;;   # ex. 520
        4??  )  Ip_Conntrack_Max=50000 ;;   # ex. 410/415/420
        6??  )  Ip_Conntrack_Max=200000 ;;   # ex. 622/625/630/635
        Aggregator )  Ip_Conntrack_Max=50000 ;;   # ex. 3G Aggregator
        240  )  Ip_Conntrack_Max=50000 ;;   # ex. Mesh 240
        400  )  Ip_Conntrack_Max=50000 ;;   # ex. Mesh 400
        700  )  Ip_Conntrack_Max=50000 ;;   # ex. Mesh 700
        320  )  Ip_Conntrack_Max=51200 ;;   # ex. 320
        220  )  Ip_Conntrack_Max=51200 ;;   # ex. 220
        12?? )  Ip_Conntrack_Max=51200 ;;  # ex. 1200 
        1420 )  Ip_Conntrack_Max=102400 ;;  # ex. 1420 
        1120 )  Ip_Conntrack_Max=153600 ;;  # ex. 1120 na-820 with 11 ports
        24?? )  Ip_Conntrack_Max=76800 ;;  # ex. 2400 
        15?? )  Ip_Conntrack_Max=102400 ;;  # ex. 1510 
        1620 )  Ip_Conntrack_Max=153600 ;;  # ex. 1620 
        1610 )  Ip_Conntrack_Max=204800 ;;  # ex. 1610 
        2600 )  Ip_Conntrack_Max=128000 ;;  # ex. 2600 
        2610 )  Ip_Conntrack_Max=128000 ;;  # ex. 2610 
        2620 )  Ip_Conntrack_Max=614400 ;;  # ex. 2620 
        27?? )  Ip_Conntrack_Max=409600 ;;  # ex. 2710 
        2820 )  Ip_Conntrack_Max=1024000 ;;  # ex. 2820 
        30?? )  Ip_Conntrack_Max=1024000 ;;  # ex. 3000 
        3620 )  Ip_Conntrack_Max=1024000 ;;  # ex. 3620 
        5000 )  Ip_Conntrack_Max=1024000 ;;  # ex. 5000 
        BL10* )  Ip_Conntrack_Max=51200 ;;   # ex. BL10800, BL10400, ...
        BL212* )  Ip_Conntrack_Max=102400 ;;   # ex. BL21200, ...
        BL216* )  Ip_Conntrack_Max=128000 ;;   # ex. BL21600, ...
	60?D )  Ip_Conntrack_Max=100000 ;;   # ex. LB604/604D/608/608D/ ...
        60? )  Ip_Conntrack_Max=100000 ;;   # ex. LB604/608/ ...
        3040 )  Ip_Conntrack_Max=1000000 ;;   # ex. LB3040 ...
        3080 )  Ip_Conntrack_Max=1000000 ;;   # ex. LB3080 ...
        3120 )  Ip_Conntrack_Max=1000000 ;;   # ex. LB3120 ...
        3100 )  Ip_Conntrack_Max=1000000 ;;   # ex. LB3100 ...
        3150 )  Ip_Conntrack_Max=1000000 ;;   # ex. LB3150 ...
        5150 )  Ip_Conntrack_Max=3000000 ;;   # ex. LB5150 ...
        5200 )  Ip_Conntrack_Max=3000000 ;;   # ex. LB5200 ...
        5300 )  Ip_Conntrack_Max=5000000 ;;   # ex. LB5300 ...
        * )  Ip_Conntrack_Max=50000 ;;   # ex. Other QBs, ...
    esac
fi
[ ! -z $Ip_Conntrack_Max ] && /sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_max=$Ip_Conntrack_Max

# /sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_tcp_timeout_established=120 # back to default...nancy 040930 
 /sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_tcp_timeout_established=3600 # deafult value is 432000(5days) ...20101104 brian

/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_tcp_timeout_close_wait=120

#/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_icmp_timeout=5

#20100730 For Israel healthy check case
/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_icmp_timeout=1

#/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout=5
#/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout=10
#/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout=30
#/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout_stream=10

#20080403 Brian For Sip service
#/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout=600
#/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout_stream=60

#20111115 Brian For IPSEC NAT
#/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout_stream=10
/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout_stream=60   #Creek's sip can't use 10 sec
/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_udp_timeout=5

/sbin/sysctl -w net.ipv4.ip_dynaddr=1

/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_tcp_timeout_syn_sent=50

/sbin/sysctl -w ${KERNEL_PARAMS_PREFIX}.ip_conntrack_generic_timeout=35 #Orginal value=600...brian 20070628

/sbin/sysctl -w kernel.printk="4 4 1 7" #Brian 20080327 Orginal value="6 4 1 7" To ease CPU usage

/sbin/sysctl -w vm.min_free_kbytes=5500 #Brian 20080808 Used to free cache memory

/sbin/sysctl -w net.ipv4.conf.all.arp_ignore=0 #Brian 20081028 Used to accept arp broadcast.

#20140220 Brian add Notes:
#==============================================================================================
#arp_filter
#0 - (default) The kernel can respond to ARP requests with addresses from other interfaces. This may seem wrong but it usually makes sense, because it increases the chance of successful communication. IP addresses are owned by the complete host on Linux, not by particular interfaces. Only for more complex setups like load-balancing, does this behaviour cause problems.
#1 - Allows you to have multiple network interfaces on the same subnet, and have the ARPs for each interface be answered based on whether or not the kernel would route a packet from the ARP'd IP out that interface (therefore you must use source based routing for this to work). In other words it allows control of which cards (usually 1) will respond to an ARP request. 
#==============================================================================================
#arp_announce
#The option in linux that allows you to control which source address is put in to ARP headers. 
#It can take the following values.
# 0 (default) Any local address
# 1 Use address from the same subnet as the target address
# 2 prefer primary address.
#==============================================================================================
#arp_ignore
#0 - (default) reply for any local target IP address, configured on any interface
#1 - reply only if the target IP address is local address configured on the incoming interface
#2 - reply only if the target IP address is local address configured on the incoming interface and both with the sender's IP address are part from same subnet on this interface
#3 - do not reply for local addresses configured with scope host, only resolutions for global and link addresses are replied
#4 - 7 - reserved
#8 - do not reply for all local addresses 
#==============================================================================================
for i in /proc/sys/net/ipv4/conf/*
do
    echo "1" > $i/arp_filter
    echo "1" > $i/arp_announce  #Brian 20140221 org=2 ,change to 1 may fix gw's arp not correct on qbreport.(xt_ingw.ko use it)
    echo "0" > $i/arp_ignore    #Brian 20081028 Used to accept arp broadcast.
done
echo 1 >/proc/sys/net/ipv6/conf/all/forwarding
