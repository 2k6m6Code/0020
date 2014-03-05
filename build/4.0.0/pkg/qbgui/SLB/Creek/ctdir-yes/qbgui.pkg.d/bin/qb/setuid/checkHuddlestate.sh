#set -x

#--- check device plug in -----------------------

if [ "$1" == "" ]; then
    a=`/sbin/lsusb |/bin/grep "Huddle"`
    b=$?
    usbcount=0
    AllNICs=`/sbin/ip addr|grep -e usb[0-9]*:|awk -F ":" '{print $2}'`
    for nic in $AllNICs
    do
        /sbin/ifconfig $nic up
        usbcount=`expr $usbcount + 1`
    done
fi
#------------------------------------------------
#
#  
#------------------------------------------------
if [ "$1" == "up" ]; then
    echo "100000000000" >/tmp/fifo.qbserv
fi

echo $usbcount>/tmp/wimaxcount
echo $b

