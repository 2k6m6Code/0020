#!/bin/sh
#set -x
echo Starting HC25 initialization script


PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
NAME="siemens HC15"
DESC="driver modules for HC15"
SCRIPT=/ect/init.d/$NAME

d_detect(){
	echo "in function detect"
	while [ `lsusb | grep -c ":"` -lt 1 ]
	do sleep 1
        lsusb
        result=$?
        if [ $result == '127' ]; then
        break;
        fi
	done
	lsusb
	#case `lsusb | grep -o "0681:[0-9][0-9][0-9][0-9]"` in
	case `lsusb | grep "0681:[0-9][0-9][0-9][0-9]" | awk '{print $6}'` in
		0681:0040)
			echo found HC25 MdmNet
			#modprobe usbserial vendor=0x0681 product=0x0040
			/sbin/insmod /lib/modules/2.6.17.7/kernel/drivers/usb/serial/usbserial.ko vendor=0x0681 product=0x0040
			sleep 2
			echo send at^susb
			echo AT^SUSB="Startup","Mdm" > /dev/ttyUSB0
			sleep 1
			echo reset module
			echo AT+CFUN=1,1 > /dev/ttyUSB0
			echo remove usb serial
			rmmod usbserial
			sleep 2
			d_detect
		;;
		0681:0047)
			echo found HC25 Mdm
                        rmmod usbserial 2>/dev/null || true
                        rmmod cdc_acm  2>/dev/null || true
	                echo "load kernel modules cdc_acm"
                        insmod /lib/modules/2.6.17.7/kernel/drivers/usb/class/cdc-acm.ko

			echo load usbserial kernel module
			/sbin/insmod /lib/modules/2.6.17.7/kernel/drivers/usb/serial/usbserial.ko vendor=0x0681 product=0x0047
			#modprobe usbserial vendor=0x0681 product=0x0047
			echo "HC25 is reachable over /dev/ttyUSB0 (application port) and /dev/ttyACM0 (modem port)"
		;;
		0681:0041)
			echo Hc25 detected as mass storage
			exit 3
		;;
		*)
			echo no HC15 detected
			exit 2
		;;
	esac
}

d_start(){
#	echo "load kernel modules cdc_acm"
#        insmod /lib/modules/2.6.17.7/kernel/drivers/usb/class/cdc-acm.ko
	d_detect
}

d_stop(){
	echo "delete kernel modules usbserial and cdc_acm"
	rmmod usbserial 2>/dev/null || true
	rmmod cdc_acm  2>/dev/null || true
}

case $1 in
	start|restart)
		echo "starting $DESC: $NAME"
		#d_stop
		#sleep 1
		d_start
		echo done;
	;;
	stop)
		echo "stopping $DESC: $NAME"
		d_stop;
		echo done;
	;;
	*)
		echo "usage: $SCRIPT {start|stop|restart}" >&2
		exit 1
	;;
esac

exit 0
	
