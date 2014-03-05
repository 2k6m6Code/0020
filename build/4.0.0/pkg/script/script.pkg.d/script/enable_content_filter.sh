#!/bin/sh
#..........................................................
# luke
# * To start squid proxy server.
#..........................................................
#set -x
killall -9 squid
SQUIDPXY="/mnt/squid.pkg"
SQUIDCFG="/usr/local/apache/qbconf/squidgen.xml"
if [ -f $SQUIDPXY ]; then
   enablesquid=`grep -c isenable=\"1\" $SQUIDCFG`
   #pxyhttpportno=`grep pxyhttpportno $SQUIDCFG|sed -e "s/<opt.*pxyhttpportno=\"//"|sed -e "s/\".*//"`
   if [ $enablesquid = '1' ]; then
       if [ ! -d /usr/local/squid ]; then
         tar zxfC $SQUIDPXY /usr/local/
         mkdir /etc/squid
         ln -s /usr/local/squid/etc/squid.conf /etc/squid/squid.conf
         ln -s /usr/local/squid/etc/squid /etc/init.d/squid
         mkdir /var/log/squid
         chown squid:squid /var/log/squid
         #ln -s /usr/local/squid/libexec/libbind.so.4 /usr/lib/
         #ln -s /usr/local/squid/sbin/squid /usr/sbin/
       fi
       cp -a /usr/local/squid/etc/squid.conf.default /usr/local/squid/etc/squid.conf
       /usr/local/apache/qb/setuid/do_qbcontent.pl
       /usr/local/apache/qb/setuid/do_qbsquidgen.pl
       /usr/local/apache/qb/setuid/do_qbsquidurl.pl
       /usr/local/apache/qb/setuid/do_qbsquidfile.pl
       sleep 6 
       iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 3128
       /usr/local/squid/etc/remark
       /usr/local/squid/sbin/squid
       /usr/local/squid/etc/content.sh
       /usr/local/squid/sbin/squid -k reconfigure
   fi
fi

