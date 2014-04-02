#!/bin/sh
#..........................................................
# 2008-0416 Brian
# * To start squid proxy server.
#..........................................................
#set -x
#Run=`ps -ef|grep -c RunCache`
#if [ "$Run" = "1" ];then
#   exit
#fi
/usr/local/squid/etc/delproxy.sh
killall -9 RunCache
killall -9 squid
/usr/local/squid/etc/squidstop
SQUIDPXY="/mnt/squid.pkg"
SQUIDCFG="/usr/local/apache/qbconf/pxyinit.xml"
FILTERCFG="/usr/local/apache/qbconf/squidgen.xml"
enablesquidpxy=`grep enablepxy $SQUIDCFG|sed -e "s/<opt.*enablepxy=\"//"|sed -e "s/\".*//"`
enablesquidfilter=`grep -c isenable=\"1\" $FILTERCFG`
isLB=`grep LB /mnt/conf/pkginfo`
#if [ "$isLB" != "" ];then
#  enablesquidfilter="0";
#fi

if [ "$enablesquidpxy" != "1" ] && [ "$enablesquidfilter" != "1" ]; then
    exit
fi

if [ -f $SQUIDPXY ]; then
    if [ ! -d /usr/local/squid ];then
        #tar zxfC $SQUIDPXY /usr/local/
        mkdir /etc/squid
        ln -s /usr/local/squid/etc/squid.conf /etc/squid/squid.conf
        ln -s /usr/local/squid/etc/squid /etc/init.d/squid
        #ln -s /usr/local/squid/libexec/libbind.so.4 /usr/lib/
        #ln -s /usr/local/squid/sbin/squid /usr/sbin/
    fi

	cp -a /usr/local/squid/etc/squid.conf.nocache /usr/local/squid/etc/squid.conf
	if [ "$enablesquidpxy" = "1" ];then
        #service squid start
	ismnt=`mount|grep tclog|grep ext` #check /mnt/tclog is mount on SHD.
        if [ "$ismnt" != "" ]; then
            cp -a /usr/local/squid/etc/squid.conf.default /usr/local/squid/etc/squid.conf
#            /usr/local/apache/qb/setuid/do_qbpxyinit.pl
		fi
/usr/local/apache/qb/setuid/do_qbpxyinit.pl
   fi
	
	if [ ! -d /usr/local/squid/var ];then
		#mkdir /mnt/tclog/squid
		#mkdir /mnt/tclog/squid/cache
		#mkdir /mnt/tclog/squid/log
		mkdir /usr/local/squid/var
		mkdir /usr/local/squid/var/cache
		mkdir /usr/local/squid/var/logs
		chown -R squid:squid /usr/local/squid/var
		chown -R squid:squid /usr/local/squid/var/cache
		chown -R squid:squid /usr/local/squid/var/logs
		#chown squid:squid /mnt/tclog/squid
		#chown squid:squid /mnt/tclog/squid/cache
		#chown squid:squid /mnt/tclog/squid/log
		sync;sync
	fi
            
#    if [ ! -d /usr/local/squid/var/cache/00 ];then
#		/usr/local/squid/sbin/squid -z
#	fi
	
#   cp -a /usr/local/squid/etc/squid.conf.default /usr/local/squid/etc/squid.conf
   /usr/local/apache/qb/setuid/do_qbremark.pl
   
   if [ "$enablesquidfilter" = "1" ];then
#        if [ "$enablesquidpxy" = "0" ];then
#  	    cp -a /usr/local/squid/etc/squid.conf.default /usr/local/squid/etc/squid.conf    
#            /usr/local/apache/qb/setuid/do_qbremark.pl
#        fi 
#	if [ -f /usr/local/squidGuard/squidGuard.conf.bak ];then
#	    cp -a /usr/local/squid/etc/squidGuard.conf.bak /usr/local/squidGuard/
#	    chown squid:squid /usr/local/squid/etc/squidGuard.conf.bak
#	fi
        /usr/local/apache/qb/setuid/do_qbcontent.pl
        /usr/local/apache/qb/setuid/do_qbsquidgen.pl
        /usr/local/apache/qb/setuid/do_qbsquidurl.pl
        /usr/local/apache/qb/setuid/do_qbfile.pl
        /usr/local/apache/qb/setuid/do_qbmime.pl
        /usr/local/apache/qb/setuid/do_qbwebfilter.pl
#		/usr/local/apache/qb/setuid/svsquildlog.pl
        
        #/usr/local/apache/qb/setuid/do_qbsquidfile.pl
        #/usr/local/apache/qb/setuid/do_qbcategory.pl
        /usr/local/squid/etc/content.sh
   fi
   
#   if [ "$enablesquidpxy" = "1" ] && [ "$ismnt" == "" ] && [ "$enablesquidfilter" != "1" ];then
#  	exit 
#   fi
   if [ "$enablesquidpxy" != "1" ] && [ "$enablesquidfilter" != "1" ];then
  	exit 
   fi
	mkdir /mnt/tclog/squid/cache
	chown -R squid:squid /usr/local/squid/var
	chown -R squid:squid /mnt/tclog/squid/cache
	chown -R squid:squid /usr/local/squid/var/cache
	chown -R squid:squid /usr/local/squid/var/logs

/usr/local/apache/qb/setuid/svsquildlog.pl   
   if [ ! -d /mnt/tclog/squid/cache/00 ];then
                    /usr/local/squid/sbin/squid -z
   fi
            
#   if [ "$isStart" != "" ];then
#       /usr/local/squid/sbin/squid 
#       /usr/local/squid/sbin/squid -k reconfigure
#   else 
       /usr/local/squid/sbin/RunCache &
       /usr/local/squid/sbin/squid -k reconfigure
#   fi
   /usr/local/squid/etc/proxy.sh
   /sbin/ip route flush cache
   /sbin/ip route flush cache
fi

