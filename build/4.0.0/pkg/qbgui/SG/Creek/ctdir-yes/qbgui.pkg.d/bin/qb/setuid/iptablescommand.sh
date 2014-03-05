#set -x

ad=$1
casee=$2
nic=$3
systemip=$4
value=$5
gateway=$6

case $casee in
      eth )
         iptables -t nat $ad POSTROUTING -o $nic -m mark --mark $value -m gw --gw $gateway -j SNAT --to-source $systemip
	 ;;
      ppp )
	 #iptables -t nat $ad PREROUTING -i $nic -j DROP
	 #iptables -t nat $ad POSTROUTING -o $nic -j DROP
	 #iptables -t nat $ad OUTPUT -o $nic -j DROP
	 iptables $ad PREROUTING -i $nic -j DROP
	 iptables $ad POSTROUTING -o $nic -j DROP
	 iptables $ad OUTPUT -o $nic -j DROP
	 ;;
      dropip )
	 iptables -t nat $ad PREROUTING -s $systemip -j DROP
	 iptables -t nat $ad POSTROUTING -s $systemip -j DROP
	 iptables -t nat $ad OUTPUT -s $systemip -j DROP
	 iptables -t nat $ad PREROUTING -d $systemip -j DROP
	 iptables -t nat $ad POSTROUTING -d $systemip -j DROP
	 iptables -t nat $ad OUTPUT -d $systemip -j DROP
	 ;;
esac
#----------------------------------------------------------------------
#
# 2013 01 03 
#
#   for enabled/disable
#   restart qbserv
#
#----------------------------------------------------------------------
if [ "$ad" == "-D" ]; then
echo "100000000000" >/tmp/fifo.qbserv
fi



#iptables -t nat -A POSTROUTING -o eth0 -m mark --mark 0x865271F -m gw --gw 218.211.253.254 -j SNAT --to-source 218.211.253.70

#iptables -t nat -I PREROUTING -i eth0 -j DROP
#iptables -t nat -I POSTROUTING -o eth0 -j DROP
#iptables -t nat -I OUTPUT -o eth0 -j DROP

#iptables -t nat -I PREROUTING -s IP -j DROP
#iptables -t nat -I OUTPUT -s IP -j DROP
