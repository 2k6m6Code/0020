#! /bin/sh
#set -x
#unalias /bin/cp
#unalias /bin/rm

R_LEVEL=$1

CLEAN_FLAG="NO"
LOGFILECHECKLIST=/mnt/conf/qbmonlst.con
QBLOGFILE=/var/log/qbalancer.log
DAEMONLOGFILE=/var/log/daemon.log
IPCHANGELOGFILE=/var/log/ipchange.log
DIAGLOGFILE=/var/log/diagnose.log 
LINKLOGFILE=/mnt/log/link.log
ALERTLOGFILE=/mnt/log/alert.log
SNMPDLOGFILE=/var/log/snmpd.log 
RUNWAYLOGFILE=/mnt/log/runway.log 
LOGBUGFILE=/mnt/log/LogBug.log
EZIO_PRINT_DEFAULT="/opt/qb/qbwdt/ezio"
EZIO_PRINT="/opt/qb/qbwdt/ezio -c 1 -t "
TrafficLOG="/mnt/tclog/traffic.log"
ServiceLOG="/mnt/tclog/service.log"
TrafficLOG0="/mnt/tclog/traffic0.log"
ServiceLOG0="/mnt/tclog/service0.log"
WtmpLOG="/var/log/wtmp"
PPPOECHK="/tmp/pppoechking"
CATEGORYLOG="/usr/local/squidGuard/log/squidGuard.log" 
BLOCKLOG="/usr/local/squidGuard/log/blockaccesses" 
OVERVIEWCONFIG="/usr/local/apache/qbconf/overview.xml"
ZONECONFIG="/usr/local/apache/active/zonecfg.xml"
QBREG_FILE=/opt/qb/registry
USERLOGFILE=/mnt/log/user.log
LATENCYLOGFILE=/var/log/latency.log
PKTLOSSLOGFILE=/var/log/pktloss.log

#For Analyser and Appliance Registration 
chmod 777 /tmp

# clean mail queue

rm -rf /var/spool/mqueue/*

if [ -f "/tmp/basiclock" ];then
    current_time=`date +"%s"`
    basiclock_time=`date -r /tmp/basiclock +"%s"` 
    remaintime=$(($current_time - $basiclock_time))  
    if [ ${remaintime} -ge 300 ];then
       rm -f /tmp/basiclock
    fi
fi

INFO1=`df |grep /mnt/tclog |awk '{print $5}'`
DATA_CHECK=`echo $INFO1|sed "s/%//g"`
LIMIT_ref=`cat /mnt/conf/registry |grep LIMIT`
LIMIT=`echo $LIMIT_ref|sed "s/##LIMIT//g"`
if [ $DATA_CHECK -ge $LIMIT ];then
    Oldest_filename=$(ls /mnt/tclog/ispnet|awk NR==1)
    rm -f /mnt/tclog/ispnet/$Oldest_filename
    rm -rf /mnt/tclog/nfcapd/*
fi

# check ram disk size
disk_percentage=$(df| awk '/root/ {print $5}'|sed -e "s/\%//")
if [ $disk_percentage -ge 95 ]; # disk size >= 95% need to clean the data of Historical Traffic
then
     #To delete the oldest file
     Oldest_filename=$(ls /tmp/ispnet|awk NR==1)
     rm -f /tmp/ispnet/$Oldest_filename
fi

disksize=$(df| awk '/root/ {print $4}')
#( $EZIO_PRINT "Ramdisk left:[ ${disksize} KB ]"; sleep 60; $EZIO_PRINT_DEFAULT) &

if [ $disksize -le 2048 ]; # disk size <= 2MB
then
        echo $(date) "Ramdisk is smaller than 2 mb, self-terminate." >> $QBLOGFILE
	cp -f $QBLOGFILE /mnt/log/qbalance.log
	sync
	CLEAN_FLAG="YES"
fi

if [[ $R_LEVEL = "0" || $CLEAN_FLAG = "YES" ]];
then
	echo "CLEAN LEVEL 0"
	rm -rf /tmp/qbnethis/*	
	rm -rf /tmp/ispnet/*
	cat /dev/null > $QBLOGFILE
	cat /dev/null > $DIAGLOGFILE
        cat /dev/null > /var/log/daemon.log   #Brian 20081210 Upload pkg to qb need to delete this log to free ramdisk space.
        rm -rf /opt/qb/bin/script/*.pkg  #Brian 20081210 Upload pkg to qb need to delete some garbage to free ramdisk space.

	sync
	exit 0
fi



# check qbalancer.log file size

if [ -f $QBLOGFILE ];
then
	fsize=$(ls -al $QBLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 2000000 ]; # file size >=2 MB
	then
		echo "$QBLOGFILE >= 2MB "
		cp -f $QBLOGFILE /mnt/log/qbalance.log
		sync
		cat /dev/null > $QBLOGFILE
	fi
fi

# check daemon.log file size
if [ -f $DAEMONLOGFILE ];
then
	fsize=$(ls -al $DAEMONLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 300000 ]; # file size >=300 KB
	then
		echo "$DAEMONLOGFILE >= 300KB "
		cp -f $DAEMONLOGFILE /mnt/log/daemon.log
		sync
		cat /dev/null > $DAEMONLOGFILE
	fi
fi

# check latency.log file size
if [ -f $LATENCYLOGFILE ];
then
	fsize=$(ls -al $LATENCYLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 300000 ]; # file size >=300 KB
	then
		echo "$LATENCYLOGFILE >= 300KB "
		cp -f $LATENCYLOGFILE /mnt/log/latency.log
		sync
		cat /dev/null > $LATENCYLOGFILE
	fi
fi

# check pktloss.log file size
if [ -f $PKTLOSSLOGFILE ];
then
	fsize=$(ls -al $PKTLOSSLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 300000 ]; # file size >=300 KB
	then
		echo "$PKTLOSSLOGFILE >= 300KB "
		cp -f $PKTLOSSLOGFILE /mnt/log/pktloss.log
		sync
		cat /dev/null > $PKTLOSSLOGFILE
	fi
fi

# check user.log file size
if [ -f $USERLOGFILE ];
then
	fsize=$(ls -al $USERLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 100000 ]; # file size >=100 KB
	then
		echo "$USERLOGFILE >= 300KB and deleted the first 5 lines"
		sed -i '1,5d' /mnt/log/user.log
		sync
	fi
fi

# check /tmp/ppplog file size
if [ -d /tmp/ppplog ];
then
	fsize=$(du /tmp/ppplog|tr -s " "|cut -f5 -d" "|sed -e "s/\/tmp\/ppplog//")
	if [ $fsize -ge 600 ]; # file size >=600 KB
	then
		echo "/tmp/ppplog >= 600KB "
		cp -f /tmp/ppplog /mnt/log/
		sync
		rm -f /tmp/ppplog/*
	fi
fi

# check ipchange.log file size
if [ -f $IPCHANGELOGFILE ];
then
	fsize=$(ls -al $IPCHANGELOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 300000 ]; # file size >=300 KB
	then
		echo $(date) "$IPCHANGELOGFILE >= 300KB " >>$RUNWAYLOGFILE
		cp -f $IPCHANGELOGFILE /mnt/log/ipchange.log
		sync
		cat /dev/null > $IPCHANGELOGFILE
	fi
fi

#20130812 Brian check LogBug.log file size
if [ -f $LOGBUGFILE ];
then
    fsize=$(ls -al $LOGBUGFILE |tr -s " "|cut -f5 -d" ")
    if [ $fsize -ge 300000 ]; # file size >=300 KB
    then
        echo $(date) "$LOGBUGFILE >= 300KB " >>$RUNWAYLOGFILE
        cat /dev/null > $LOGBUGFILE
        sync
    fi
fi

# check traffic.log file size
if [ -f $TrafficLOG ];
then
	fsize=$(ls -al $TrafficLOG |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 500000000 ]; # file size >=500 MB
	then
		echo $(date) "$TrafficLOG >= 500MB " >>$RUNWAYLOGFILE
		filename=`date +%s`
		cp -f $TrafficLOG /mnt/tclog/tc_$filename.log
		cat /dev/null > $TrafficLOG
		sync
	fi
fi
# check traffic0.log file size
if [ -f $TrafficLOG0 ];
then
	fsize=$(ls -al $TrafficLOG0 |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 2000000000 ]; # file size >= 2 GB
	then
		echo $(date) "$TrafficLOG0 >= 2GB " >>$RUNWAYLOGFILE
		filename=`date +%s`
                /sbin/service syslog stop
		mv $TrafficLOG0 /mnt/tclog/tc0_$filename.log
                /sbin/service syslog start
		sync
	fi
fi
# check service.log file size
if [ -f $ServiceLOG ];
then
	fsize=$(ls -al $ServiceLOG |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 500000000 ]; # file size >=500 MB
	then
		echo $(date) "$ServiceLOG >= 100MB " >>$RUNWAYLOGFILE
		filename=`date +%s`
		cp -f $ServiceLOG /mnt/tclog/tc_$filename.log
		cat /dev/null > $ServiceLOG
		sync
	fi
fi
# check service0.log file size
if [ -f $ServiceLOG0 ];
then
	fsize=$(ls -al $ServiceLOG0 |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 2000000000 ]; # file size >=2 GB
	then
		echo $(date) "$ServiceLOG0 >= 2GB " >>$RUNWAYLOGFILE
		filename=`date +%s`
                /sbin/service syslog stop
		mv $ServiceLOG0 /mnt/tclog/tc0_$filename.log
                /sbin/service syslog start
		sync
	fi
fi


# check link.log file size
if [ -f $LINKLOGFILE ];
then
	fsize=$(ls -al $LINKLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 100000 ]; # file size >=100 KB
	then
		cat /dev/null > $LINKLOGFILE
		echo $(date) "$LINKLOGFILE >= 100KB " >>$RUNWAYLOGFILE
		sync
	fi
fi

# check wtmp log file size
if [ -f $WtmpLOG ];
then
	fsize=$(ls -al $WtmpLOG |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 100000 ]; # file size >=100 KB
	then
		cat /dev/null > $WtmpLOG
		echo $(date) "$WtmpLOG >= 100KB "
		sync
	fi
fi

# check alert.log file size
if [ -f $ALERTLOGFILE ];
then
	fsize=$(ls -al $ALERTLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 600000 ]; # file size >=600 KB
	then
		cat /dev/null > $ALERTLOGFILE
		echo $(date) "$ALERTLOGFILE >= 600KB " >>$RUNWAYLOGFILE
		sync
	fi
fi

#/opt/qb/bin/script/test.sh
#sync

# check snmpd.log file size

if [ -f $SNMPDLOGFILE ];
then
	fsize=$(ls -al $SNMPDLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 400000 ]; # file size >= 400KB
	then
		echo "$SNMPDLOGFILE >= 400KB "
		cp -f $SNMPDLOGFILE /mnt/log/snmpd.log
		sync
		cat /dev/null > $SNMPDLOGFILE
	fi
fi

# check diagnose.log file size

if [ -f $DIAGLOGFILE ];
then
	fsize=$(ls -al $DIAGLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 1000000 ]; # file size >= 1 MB
	then
		echo "$DIAGLOGFILE >= 1MB "
		cp -f $DIAGLOGFILE /mnt/log/diagnose.log
		sync
		cat /dev/null > $DIAGLOGFILE
	fi
fi

#check 3proxy log
PROXY3LOG="/usr/local/etc/3proxy/logs"

if [ -d $PROXY3LOG ];
then
	#fsize=$(ls -al $PROXY3LOG |tr -s " "|cut -f5 -d" ")
	fsize=`du -l $PROXY3LOG|awk '{print $1}'`
	if [ "$fsize" -ge 300 ]; # file size >= 300KB
	then
		echo "$PROXY3LOG >=  300KB"
		cd $PROXY3LOG
		for file in $(ls)
		do
		    cat /dev/null > $file
		done
		cd -
	fi
fi

# check squidguard file size

if [ -f $CATEGORYLOG ];
then
	fsize=$(ls -al $CATEGORYLOG |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 1000000 ]; # file size >=300 KB
	then
		echo "$CATEGORYLOG >= 300KB "
		cp -f $CATEGORYLOG /mnt/log/squidg.log
		sync
		cat /dev/null > $CATEGORYLOG
	fi
fi

if [ -f $BLOCKLOG ];
then
	fsize=$(ls -al $BLOCKLOG |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 1000000 ]; # file size >=300 KB
	then
		echo "$BLOCKLOG >= 300KB "
		cp -f $BLOCKLOG /mnt/log/block.log
		sync
		cat /dev/null > $BLOCKLOG
	fi
fi

CACHELOG="/usr/local/squid/var/logs/cache.log"
if [ -f $CACHELOG ];
then
        fsize=$(ls -al $CACHELOG |tr -s " "|cut -f5 -d" ")
        if [ $fsize -ge 300000 ]; # file size >=300 KB
        then
                echo "$BLOCKLOG >= 300KB "
                #cp -f $BLOCKLOG /mnt/log/block.log
                #sync
                cat /dev/null > $CACHELOG
        fi
fi

# check runway.log file size

if [ -f $RUNWAYLOGFILE ];
then
	fsize=$(ls -al $RUNWAYLOGFILE |tr -s " "|cut -f5 -d" ")
	if [ $fsize -ge 1000000 ]; # file size >= 1 MB
	then
		echo "$RUNWAYLOGFILE >= 1MB "
		cat  /dev/null > $RUNWAYLOGFILE
	fi
fi

# check pppoe flag file

if [ -f $PPPOECHK ];
then
        PPPOECHK_TIME=`date -r $PPPOECHK +%s`
        CURRENT_TIME=`date +%s`
        let PPPOECHK_TIME=$PPPOECHK_TIME+600
	if [ $CURRENT_TIME -ge $PPPOECHK_TIME ]; # >10 min
	then
		echo "Delete PPPoE Check flag ..."
                rm -rf $PPPOECHK
	fi
fi

# chek if LOGFILECHECKLIST=/mnt/conf/qbmonlst.con exists
# if it does exist, we will delete all the files listed in it
# Caution: every file listed qbmonlst.con is very sure to be deleted 

if [ -f $LOGFILECHECKLIST ]
then
    for file in $(cat $LOGFILECHECKLIST)
    do
        if [ $file = "/" ]
        then
            continue
        fi

        if [[ -d $file ]]
        then
            rm -rf $file
        fi
        
        if [[ -f $file ]]
        then
            cat /dev/null > $file
        fi
    done
fi

#Need terminfo=dumb
/opt/qb/bin/script/cputest &
/opt/qb/bin/script/qbserv.chk &
/opt/qb/hsdpa/dailyrst3g &

#for cpulimit
MOUNTDEV=`grep analydev $OVERVIEWCONFIG|sed -e "s/<opt.*analydev=\"//"|sed -e "s/\".*//"`
cpulimit_count=`ps -ef|grep -v grep|grep -c cpulimit_daemon.sh `
if [ -d /mnt/tclog/analyser/etc/httpd ] && [ "$MOUNTDEV" != "" ] && [ "$cpulimit_count" = "0" ];then
/sbin/cpulimit_daemon.sh &
fi

#20100628 Brian qbcli sometimes occupy 99% CPU usage
CLI_CPU=`/usr/bin/top -n 1 -b|grep qbcli|awk NR==1|awk '{print $( 9 )*100 }'`
if [ $CLI_CPU -ge 3000 ]; # The CPU usage of process >=90%
then
    killall -9 qbcli
fi

#20111226 Brian Check httpd is alive or not
HTTPD_num=`ps -ef|grep -c httpd`
if [ $HTTPD_num -le 3 ];then # If the httpd process <=3,means httpd is not working
   /sbin/service httpd restart
   echo $(date) "Httpd processes restarted" >>$RUNWAYLOGFILE
fi

#20120119 Brian Check sshd is alive or not
SSHD_num=`ps -ef|grep sbin|grep -c sshd`
if [ $SSHD_num -le 0 ];then # If the sshd process <=0,means sshd is not working
   /sbin/service sshd restart
   echo $(date) "sshd processes restarted" >>$RUNWAYLOGFILE
fi

#20131209 Brian Check ARPPROXY is used or not #20131211 Mark it
#ARPPROXY_num=`cat $ZONECONFIG|grep -c ARPPROXY`
#if [ $ARPPROXY_num -ge 1 ];then
#   /usr/local/apache/qb/setuid/do_qbarp.pl &
#fi

EZIO=$(awk "/EZIOTYPE/ {print \$2}"  $QBREG_FILE)
if [ "$EZIO" = "1" ];then
  Hostname=`grep hostname_lcm $OVERVIEWCONFIG|sed -e "s/<opt.*hostname_lcm=\"//"|sed -e "s/\".*//"`
  if [ "$Hostname" != "192.168.1.254" ] && [ "$Hostname" != "" ];then # show hostname
   ( $EZIO_PRINT "Ramdisk left:[ ${disksize} KB ]"; sleep 60; $EZIO_PRINT "Hostname:$Hostname" ; sleep 60 ; $EZIO_PRINT_DEFAULT ) &
  else
   ( $EZIO_PRINT "Ramdisk left:[ ${disksize} KB ]"; sleep 60; $EZIO_PRINT_DEFAULT) &
  fi
fi

#******************************************************************
# 2014-0320
# Gary check SHD exist or not
#
# if does not exist , clear /mnt/tclog/nfcapd/*  and kill nfcapd daemon
#
#******************************************************************
if [ -f "/tmp/SHD_healthy_OK" -a ! -f /tmp/SHD_not_found -a ! -f /tmp/SHD_Crash -a ! -f /tmp/SHD_failed ];then

    SHD=`df -h | grep tclog$ | awk '{print $1}'`
    touch /mnt/tclog/nfcapd/test_SHD
    if [ "$SHD" = "" ]; then
    	killall -9 nfcapd
    	rm -rf /mnt/tclog/nfcapd
    	rm -f /tmp/SHD_healthy_OK
    	sync
        touch /tmp/SHD_failed
        echo $(date) "SHD failed ...">>/mnt/log/bootlog
        /opt/qb/bin/script/rebootmail.sh
    elif [ ! -f "/mnt/tclog/nfcapd/test_SHD" ]; then
    	killall -9 nfcapd
    	rm -f /tmp/SHD_healthy_OK
    	touch /tmp/SHD_Crash
    	echo $(date) "SHD Crash ...">>/mnt/log/bootlog
        /opt/qb/bin/script/rebootmail.sh
    else
        #echo $(date) "check SHD healthy OK  ...">>/mnt/log/bootlog
        rm -f /mnt/tclog/nfcapd/test_SHD
    fi 
fi
#******************************************************************
# 2014-0324
# Gary check filesystem read-only or not
#
#******************************************************************
    
    FileSystem=`df -h | grep /mnt$ | awk '{print $1}'`
    
    if [ ! -f "/tmp/Please_arrage_reboot" ]; then
    	touch /mnt/test_readonly_or_not
    	echo $(date) "Check filesystem read-only $FileSystem $Readonly" >> /mnt/log/bootlog
                    
        if [ ! -f "/mnt/test_readonly_or_not" ]; then
           /sbin/fsck.msdos -a -w $FileSystem
           echo $(date) "Fix read-only done.">>/mnt/log/bootlog
           touch /tmp/Please_arrage_reboot
           /opt/qb/bin/script/rebootmail.sh
        else
           echo $(date) "Filesystem healthy ok." >> /mnt/log/bootlog
        fi

        /bin/rm -f /mnt/test_readonly_or_not
    fi
    

#******************************************************************
# 2014-03246
# Gary keep /proc/meminfo 
#
#******************************************************************
    cat /proc/meminfo > /mnt/log/meminfo
    sync

    
#******************************************************************
# 2014-03246
# Gary check /etc/httpd/logs/error_log size
#
#******************************************************************
    MAXIMUM=5000   # 5MB
    NOW_ERROR_LOG_SIZE=`du /etc/httpd/logs/error_log | awk '{print $1}'`
    if [ "$NOW_ERROR_LOG_SIZE" -gt "$MAXIMUM" ]; then
    cat /dev/null > /etc/httpd/logs/error_log
    fi
    
