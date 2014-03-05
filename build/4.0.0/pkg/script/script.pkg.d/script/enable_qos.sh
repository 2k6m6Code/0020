#------------------------------------------------------
#for traffic and dynamic QoS
#------------------------------------------------------
#/bin/sh /usr/local/apache/active/tcscript
/usr/local/apache/active/delall
/bin/sh /usr/local/apache/active/dqos.sh
# NEW QoS
#if [ -f /usr/local/apache/qbconf/qosh ];then
    /sbin/ip route flush cache
    /sbin/ip route flush cache
    #Shane's QOS doesn't need qbimq del
    #/opt/qb/bin/script/qbimq del
    /usr/local/apache/active/qosinit
    /usr/local/apache/active/qos.sh
    /usr/local/apache/active/qoslan.sh
    /usr/local/apache/active/qosisp.sh
#fi

