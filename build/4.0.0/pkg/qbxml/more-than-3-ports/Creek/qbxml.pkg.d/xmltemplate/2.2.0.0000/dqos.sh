#!/bin/sh  

/usr/local/sbin/iptables -t mangle -X DEF 
/usr/local/sbin/iptables -t mangle -N DEF 
/usr/local/sbin/iptables -t mangle -X COD 
/usr/local/sbin/iptables -t mangle -N COD 
/usr/local/sbin/iptables -t mangle -X PSD 
/usr/local/sbin/iptables -t mangle -N PSD 
/usr/local/sbin/iptables -t mangle -X ICMP 
/usr/local/sbin/iptables -t mangle -N ICMP 
/usr/local/sbin/iptables -t mangle -A COD -p tcp --syn -m connlimit --connlimit-above 50 -m limit -j LOG --log-level alert  --log-prefix cod:connectionoverflow
/usr/local/sbin/iptables -t mangle -A COD -j ICMP 

/usr/local/sbin/iptables -t mangle -A DEF -j ACCEPT 

/usr/local/sbin/iptables -t mangle -A INPUT -p icmp -j ICMP 

/usr/local/sbin/iptables -t mangle -A INPUT -p tcp -j COD 

