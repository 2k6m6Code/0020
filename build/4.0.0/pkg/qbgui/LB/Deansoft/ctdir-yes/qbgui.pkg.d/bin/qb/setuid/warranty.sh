#! /bin/sh

INITDATE_file="/mnt/conf/init.dat"
rm -f /tmp/init*
cp -f $INITDATE_file  /tmp/init.nc
/usr/bin/mcrypt -d /tmp/init.nc -k 2k6m6$ >/dev/null 2>&1
echo "Original Info:"
cat /tmp/init|grep Firmware
cat /tmp/init|grep MAC
#Get time info
Shipment_time=`cat /tmp/init|grep 'Shipment'|awk '{print $2}'|sed -e "s/\n//"`
Register_time=`cat /tmp/init|grep 'Register'|awk '{print $2}'|sed -e "s/\n//"`
Warranty_time=`cat /tmp/init|grep 'Warranty'|awk '{print $2}'|sed -e "s/\n//"|sed 's/\n//g'`
 
Shipment_date=`date -d "1970-01-01 UTC $Shipment_time seconds" +"%Y-%m-%d"`
Register_date=`date -d "1970-01-01 UTC $Register_time seconds" +"%Y-%m-%d"`
echo Shipment_date $Shipment_date
echo Register_date $Register_date
  
count=0
for time in $Warranty_time
do
    Warranty_date=`date -d "1970-01-01 UTC $time seconds" +"%Y-%m-%d"`
    echo Warranty_date_0$count $Warranty_date
    let count=$count+1
done
