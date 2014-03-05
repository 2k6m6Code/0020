ip=$1
warrantysh="/usr/local/apache/qb/setuid/warranty.sh"
sn=`cat /mnt/conf/qbsn`
info=`cat /mnt/conf/pkginfo|grep DETAIL`
image=`cat /mnt/conf/image.ifo|grep serial|tail -n 1`
#fs=`date -r /mnt/image.gz`
fs=`cat /mnt/conf/fsimage.ifo|grep version|tail -n 1`
regist=`$warrantysh |grep Register_date`
warranty=`$warrantysh |grep Warranty_date`
upgradestate=`cat /tmp/upgradestate`
a=`uptime|awk -F ',' '{print $1}'|awk '{print $4}'`
if [ "$a" == "days" ] || [ "$a" == "day" ]; then
	uptime=`uptime |awk '{print $3 $4 $5}'|sed -e "s/\,/ /"|sed -e "s/\,//"`
else
	uptime=`uptime |awk '{print $3}'|sed -e "s/\,//"`
fi
reboot_time=`cat /tmp/reboot_time`
if [ "$upgradestate" == "" ]; then
    upgradestate="None"
fi
echo $sn\;
echo $info\; 
echo $image\; 
echo $fs\;
echo $regist\;
echo $warranty\;
echo $upgradestate\;
echo $uptime\;
echo $reboot_time\;
#killall -9 sleep
