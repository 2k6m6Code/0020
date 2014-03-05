#!/bin/bash
#set -x
PROXY="/usr/local/apache/qbconf/httproxy.sh"
TMPSH="/usr/local/apache/qbconf/tmp.sh"
BASICXML="/usr/local/apache/qbconf/basic.xml"
action=$1
proxyip=$2
iid=$3

#Add new iptables rule
if [ "$action" = "add" ]; then
#Get setuped proxy info
`grep enableproxy=\"1\" $BASICXML|grep -v iid=\"$iid\"|sed -e "s/  <isp.*proxyip=\"//"|sed -e "s/\".*//" >/tmp/proxy_proxyip`

#Calculate all proxy ip
oldproxyline=`/usr/bin/nl /tmp/proxy_proxyip|tail -n 1|awk '{print $1}'`
oldproxyline=`expr $oldproxyline + 1`

#Generate a iptable command shell script
line=1
echo " ">$TMPSH
echo "/usr/local/sbin/iptables -t nat -I PREROUTING -p tcp --dport 80 -m state --state NEW -j BALANCE " >>$TMPSH
 for count in *
     do
        packetnum=`expr $line - 1`
        if test $line -ne $oldproxyline 
        then
          proxy_proxyip=`awk NR==$line /tmp/proxy_proxyip`
          echo " --to-destination $proxy_proxyip-0.0.0.1" >>$TMPSH
          line=`expr $line + 1`
        else
          echo " --to-destination $proxyip-0.0.0.1" >>$TMPSH
          /usr/bin/tr --delete "\n" <$TMPSH >$PROXY
         exit 0
         fi
     done

#Remove temporary files
rm -f /tmp/proxy_proxyip
rm -f $TMPSH
fi

#Remove disconnect link's weight
if [ "$action" = "disconnect" ]; then
disconnect_proxyip=`grep enableproxy=\"1\" $BASICXML|grep -v iid=\"$iid\"|sed -e "s/  <isp.*proxyip=\"//"|sed -e "s/\".*//"`
   if [ "$disconnect_proxyip" != "" ]; then
     `grep iptables $PROXY|sed -e "s/$disconnect_proxyip-0.0.0.1/$disconnect_proxyip-0.0.0.0/" >$TMPSH`
     `grep iptables $PROXY|sed -e "s/nat -I/nat -D/" >>$TMPSH`
     `/bin/chmod 755 $TMPSH`
     $TMPSH
   fi
fi

#Add connect link's weight
if [ "$action" = "connect" ]; then
disconnect_proxyip=`grep enableproxy=\"1\" $BASICXML|grep -v iid=\"$iid\"|sed -e "s/  <isp.*proxyip=\"//"|sed -e "s/\".*//"`
   if [ "$disconnect_proxyip" != "" ]; then
     `grep iptables $PROXY|sed -e "s/$disconnect_proxyip-0.0.0.1/$disconnect_proxyip-0.0.0.0/"|sed -e "s/nat -I/nat -D/" >$TMPSH`
     `/bin/chmod 755 $TMPSH`
     $TMPSH
     rm -f $TMPSH
     $PROXY
   fi
fi
