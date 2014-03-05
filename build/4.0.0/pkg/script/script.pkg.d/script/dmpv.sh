#!/bin/bash
#set -x
#localip=$1
#remoteip=$2
ispid=$1
ACTIVEBASICXML="/usr/local/apache/active/basic.xml"
option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ServerAliveInterval=5 -o ServerAliveCountMax=3 -o ConnectTimeout=30" 
ispinfo=`grep iid=\"$ispid\" $ACTIVEBASICXML`
systemip=`echo $ispinfo|sed -e "s/<isp.*systemip=\"//g"|sed -e "s/\".*//"`
remoteip=`echo $ispinfo|sed -e "s/<isp.*remote=\"//g"|sed -e "s/\".*//"`
localip=`echo $ispinfo|sed -e "s/<isp.*local=\"//g"|sed -e "s/\".*//"`
gateway=`echo $ispinfo|sed -e "s/<isp.*gateway=\"//g"|sed -e "s/\".*//"`
mpv_nat=`echo $ispinfo|sed -e "s/<isp.*mpv_nat=\"//g"|sed -e "s/\".*//"`
ipcom=`echo $ispinfo|sed -e "s/<isp.*ipcom=\"//g"|sed -e "s/\".*//"`
enc=`echo $ispinfo|sed -e "s/<isp.*enc=\"//g"|sed -e "s/\".*//"`
enc_alg=`echo $ispinfo|sed -e "s/<isp.*alg=\"//g"|sed -e "s/\".*//"`
if [ "$enc_alg" = "aes 128" ];then
enc_alg="aes128"
elif [ "$enc_alg" = "aes 192" ];then
enc_alg="aes192"
elif [ "$enc_alg" = "aes 256" ];then
enc_alg="aes256"
fi

while : ; do
 wanstate=`grep systemip=\"$localip\" $ACTIVEBASICXML|grep -c alive=\"1\"`

 if [ "$wanstate" = "1" ];then
 
#prevent "resource temporarily unavailable"
ispname=`echo $ispinfo|sed -e "s/<isp.*ispname=\"//g"|sed -e "s/\".*//"`
if [ "$enc" = "1" ]; then
sleep 60   #if link is down,wait if other link is connecting link.
alive=`grep "iid=\"$ispid\"" $ACTIVEBASICXML|sed -e "s/  <isp.*alive=\"//"|sed -e "s/\".*//"`
  if [ "$alive" = "1" ]; then
    exit 0
  else
    /sbin/setkey -f /etc/racoon/delipsec.$ispname
  fi
fi

   remoteip=`echo $ispinfo|sed -e "s/<isp.*remote=\"//g"|sed -e "s/\".*//"`  #Need to modify remote site,so need to get remote ip again.
   ping -I $localip $remoteip -c 2 >/dev/null #Check if resource temporarily unavailable 
   reachable1=$?
                              
   if [ "$reachable1" = "0" ];then
     if [ "$mpv_nat" = "1" ];then
       mpv_nat_ip=`echo $ispinfo|sed -e "s/<isp.*mpv_nat_ip=\"//g"|sed -e "s/\".*//"`
       new_mpv_nat_ip=`/sbin/wget -O - -q icanhazip.com --bind-address=$localip --timeout=10|sed -e "s/\n//"`
        if [ "$new_mpv_nat_ip" != "" ];then
          ssh $remoteip -i /etc/.ssh/qlogin $option "/opt/qb/bin/script/checkmpvip $systemip $new_mpv_nat_ip $gateway $remoteip $ipcom $enc $enc_alg" 2>>/tmp/$systemip
        elif [ "$mpv_nat_ip" != "" ];then 
          ssh $remoteip -i /etc/.ssh/qlogin $option "/opt/qb/bin/script/checkmpvip $systemip $mpv_nat_ip $gateway $remoteip $ipcom $enc $enc_alg" 2>>/tmp/$systemip
        fi
     else
        ssh $remoteip -i /etc/.ssh/qlogin $option "/opt/qb/bin/script/checkmpvip $systemip $localip $gateway $remoteip $ipcom $enc $enc_alg" 2>>/tmp/$systemip
     fi
   fi
#   if [ "$enc" = "1" ]; then
#   #Check if SA is exist"
#   `/sbin/setkey -DP|grep $localip|grep $remoteip >/dev/null`
#   checkSA=$?
#     if [ "$checkSA" != "0" ];then
#     /usr/local/apache/qb/setuid/do_qbipsec.pl
#     /usr/local/apache/qb/setuid/do_qbracoon.pl
#     /usr/sbin/racoonctl reload-config
#     sleep 2
#     /sbin/setkey -f /etc/racoon/ipsec.conf
#     fi
#   fi
 fi
 sleep 30
 isp=`grep iid=\"$ispid\" $ACTIVEBASICXML`
 alive=`grep iid=\"$ispid\" /usr/local/apache/active/basic.xml|grep -c "alive=\"1\""`
 if [ "$isp" = "" ] || [ "$alive" = "1" ];then
     exit
 fi
done
