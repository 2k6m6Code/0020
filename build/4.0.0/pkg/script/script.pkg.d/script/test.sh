#set -x
QB_HOME_DIR=/opt/qb
QBREG_FILE=$QB_HOME_DIR/registry
MAXISP=$(awk "/^MAXISP/ {print \$2}"  $QBREG_FILE)
NUMOFPORT=$(awk "/^NUMOFPORT/ {print \$2}"  $QBREG_FILE)
ENABLEVM=$(awk "/^ENABLEVM/ {print \$2}"  $QBREG_FILE)
ACTIVEBASICXML=/usr/local/apache/active/basic.xml
#random=$(( $RANDOM % $MAXISP ))
echo $(date) "QB Link check...">>/mnt/log/bootlog
for (( random=0; random<=$MAXISP; random=random+1 ))
do

mpvgw=`grep nic=\"mpv$random\" $ACTIVEBASICXML|sed -e "s/  <isp.*gateway=\"//"|sed -e "s/\".*//"`
if [ "$mpvgw" != "" ];then
 ping $mpvgw -c 1
 pingresult=$?
   if [ $pingresult = '1' ] ;then
   echo "Link is down!"
   continue
   fi

 /sbin/wget http://$mpvgw:4000/clean/cleanrmconfig.htm --connect-timeout=1 --tries=1 -O /tmp/chk_file
 testresult=$?
 if [ $testresult = '1' ] ;then
 sleep 5
 /sbin/wget http://$mpvgw:4000/clean/cleanrmconfig.htm --connect-timeout=1 --tries=1 -O /tmp/chk_file
  testresult1=$?
  if [ $testresult1 = '1' ] ;then
  sleep 5
  /sbin/wget http://$mpvgw:4000/clean/cleanrmconfig.htm --connect-timeout=1 --tries=1 -O /tmp/chk_file
   testresult2=$?
    if [ $testresult2 = '1' ] ;then
    echo "Find a strange link:mpv$random" >>/mnt/log/link.log
    /sbin/ifconfig mpv$random|/opt/qb/bin/script/mail -s "Find a strange link:mpv$random" vercheck@creek.com.tw
    /opt/qb/bin/script/mail.sh mpv$random
    /sbin/ifconfig mpv$random down
    sleep 3
    fi
  fi
 fi
fi

done
   
if [ -f /mnt/conf/insdate ]; then

  rm -f /mnt/conf/dtstamp.dc
  mcrypt -d /mnt/conf/dtstamp -k 2k6m6
  Seconds=`cat /mnt/conf/dtstamp.dc`
  if [ "$Seconds" = "" ] ;then 
    if [ ! -f /mnt/conf/timeup ]; then
      #Check uptime 45 days
      uptime|grep "45 days"
      if [ "$?" != "1" ];then
       /opt/qb/bin/script/mail.sh noreg
       for (( devnum=0; devnum<$NUMOFPORT -1; devnum=devnum+1 ))
       do
         /sbin/ifconfig eth$devnum down
       done
       touch /mnt/conf/timeup
       echo $(date) "45 Days Timeup!!! Need to register qb.">>/mnt/log/bootlog
      fi
    else
      #Check uptime 7 days
      uptime|grep "7 days"
      if [ "$?" != "1" ];then
       /opt/qb/bin/script/mail.sh noreg
       echo $(date) "7 Days Timeup!!! Need to register qb.">>/mnt/log/bootlog
       for (( devnum=0; devnum<$NUMOFPORT -1; devnum=devnum+1 ))
       do
         /sbin/ifconfig eth$devnum down
       done
      fi
    fi
  fi
fi

#Check vmware license
if [ $ENABLEVM = '1' ];then
/opt/qb/bin/script/licensetime_daily
fi
