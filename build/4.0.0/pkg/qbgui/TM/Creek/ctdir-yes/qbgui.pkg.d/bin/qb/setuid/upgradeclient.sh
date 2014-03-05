#!/bin/bash
set -x
remoteip=$1
num=$2
time=$3

#echo num$num >>/tmp/reip
#echo time$time >>/tmp/reip

#option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ServerAliveInterval=15"
#option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ConnectTimeout=5"
option="-o StrictHostKeyChecking=no -o TCPKeepAlive=no -o ServerAliveInterval=5 -o ServerAliveCountMax=2 -o ConnectTimeout=5"
ACTIVEBASICXML=/usr/local/apache/active/basic.xml

#echo $time >>/tmp/sch
#exit 0

isupg=`echo $num|grep upg`
sn=`grep $remoteip $ACTIVEBASICXML|sed -e "s/  <isp.*qbsn=\"//"|sed -e "s/\".*//"`
name=`grep $remoteip $ACTIVEBASICXML|sed -e "s/  <isp.*ispname=\"//"|sed -e "s/\".*//"`

#info=`grep $remoteip $ACTIVEBASICXML|sed -e "s/  <isp.*info=\"VERSIONDETAIL\://"|sed -e "s/\".*//"`
#echo $info

#remove upgrade log
/bin/rm -f /tmp/$remoteip/log
mkdir /tmp/$remoteip

#--------------------------------------------------------------------------
#    upgrade is pkg og upg
#    do_qbsavestate.pl save upgrade state Success or fail to active/basic.xml
#--------------------------------------------------------------------------
if [ "$isupg" = "" ]; then
    scp $option /tmp/$num/*.pkg $remoteip:/tmp/tmpupg/image.tmp
    #echo $(date -R) "Start upgrade client $sn through $name" >>/tmp/$remoteip/log
    ssh $option $remoteip "/usr/local/apache/qb/setuid/qbimg.sh" >>/tmp/$remoteip/log
else    
    scp $option /tmp/$num/*.upg $remoteip:/tmp/tmpupg/upload.tmp 
    info=`find  /tmp/$num/ -name *.upg`
    upgsize=`/usr/bin/du -b /tmp/$num/*.upg|sed -e "s/\/tmp.*//"`
    ssh $option $remoteip "/usr/bin/du -b /tmp/tmpupg/upload.tmp" >/tmp/check
    checksize=`cat /tmp/check|sed -e "s/\/tmp\/tmpupg\/upload.tmp//"`
    echo $upgsize
    echo $checksize
    if [ "$upgsize" != "$checksize" ]; then
        #echo "trasfer upg error" >>/tmp/$remoteip/log
        ssh $option $remoteip "rm -f /tmp/tmpupg/upload.tmp"
        ssh $option $remoteip "echo \"Transfer Error\" >/tmp/upgradestate"
        /usr/local/apache/qb/setuid/do_qbsavestate.pl $sn "Transfer Error"
        exit 1
    fi
    
    ssh $option $remoteip "/usr/local/apache/qb/setuid/qbupg.sh" >>/tmp/$remoteip/log
    ssh $option $remoteip "/usr/local/apache/qb/setuid/doupgrade.sh" >>/tmp/$remoteip/log
    ssh $option $remoteip "cat /tmp/tmpupg/upg/pkginfo" >>/tmp/$remoteip/log
    isok=`grep Error /tmp/$remoteip/log`
    error=`grep ERROR /tmp/$remoteip/log`
    if [ "$isok" != "" ] || [ "$error" != "" ]; then
        ssh $option $remoteip "rm -rf /tmp/tmpupg/upg"
        ssh $option $remoteip "echo \"Upgrade Error\" >/tmp/upgradestate"
        /usr/local/apache/qb/setuid/do_qbsavestate.pl $sn "Upgrade Error"
        exit 1
    fi

fi

#--------------------------------------------------------------------------
#    Reboot time
#--------------------------------------------------------------------------
if [ "$time" = "24" ];then
    ssh $option $remoteip "reboot"
    ssh $option $remoteip "echo \"Success\" >/tmp/upgradestate"
/bin/rm -f /tmp/$remoteip/log
elif [ "$time" = "0" ];then
    $time=24
    ssh $option $remoteip "/opt/qb/bin/script/rebootqb $time" 
    $time=0
    ssh $option $remoteip "echo $time >/tmp/reboot_time"
    ssh $option $remoteip "echo \"Success\" >/tmp/upgradestate"
/bin/rm -f /tmp/$remoteip/log
    #echo "Success" >/tmp/$remoteip/log
else
    ssh $option $remoteip "/opt/qb/bin/script/rebootqb $time" 
    ssh $option $remoteip "echo $time >/tmp/reboot_time"
    ssh $option $remoteip "echo \"Success\" >/tmp/upgradestate"
/bin/rm -f /tmp/$remoteip/log
    #echo "Success" >/tmp/$remoteip/log
fi
/usr/local/apache/qb/setuid/do_qbsavestate.pl $sn "Success" $time
