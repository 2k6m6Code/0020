#! /bin/sh
#set -x
usbdev=$1
action=$2

USBNO=`echo $usbdev|sed 's/ttyUSB//g'|sed 's/\n//g'`
if [ -f /tmp/usbdev.tab ];then
Brand=`cat /tmp/usbdev.tab|grep "$usbdev "|awk '{print $7}'`
else
Brand=`cat /tmp/usbdev.tab.bak|grep "$usbdev "|awk '{print $7}'`
fi
usbmodemtype=`grep pppoeportdev=\"$usbdev\" /usr/local/apache/active/basic.xml|sed -e "s/  <isp.*usbmodemtype=\"//"|sed -e "s/\".*//"`

case $Brand in
   Huawei )
            case $usbmodemtype in
                          E161 )
                                 AP_Port_NO=`expr $USBNO + 2`
                                 ;;
                          K4605 )
                                 AP_Port_NO=`expr $USBNO + 3`
                                 ;;
                          E1750)
                                 AP_Port_NO=`expr $USBNO + 3`
                                 ;;
                          E1762)
                                 AP_Port_NO=`expr $USBNO + 1`
                                 ;;
                          E1690)
                                 AP_Port_NO=`expr $USBNO + 3`
                                 ;;
                          E367)
                                 AP_Port_NO=`expr $USBNO + 3`
                                 ;;
                              *)
                                 AP_Port_NO=`expr $USBNO + 2`
                                 ;;
            esac 
            ;; # ex.
    Qisda )
            AP_Port_NO=`expr $USBNO - 1`
            ;; # ex.
    Sierra)
            exit 0
            ;; #doesn't support monitor port
        * )
            AP_Port_NO=`expr $USBNO - 1`
            ;; # ex.
esac

AP_device=ttyUSB$AP_Port_NO

case $action in
    signal )
            #signal=`echo -e "at+CSQ\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^+CSQ|awk '{print $2}'|sed -e "s/,99//"`
            signal=`catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+CSQ\r\n"|grep ^+CSQ|awk '{print $2}'|sed -e "s/,99//"`
            echo $signal
            if [ "$signal" = "" ];then
            #echo -e "at+CSQ\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^+CSQ|awk '{print $2}'|sed -e "s/,99//"
            catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+CSQ\r\n"|grep ^+CSQ|awk '{print $2}'|sed -e "s/,99//"
            fi
            ;;
       isp )
            #echo -e "at+COPS?\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^+COPS|sed -e "s/^+COPS.*,\"//"|sed -e "s/\".*//"|sed -e "s/^+COPS: //"
            catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+COPS?\r\n"|grep ^+COPS|sed -e "s/^+COPS.*,\"//"|sed -e "s/\".*//"|sed -e "s/^+COPS: //"
            ;;
      cell )
            #echo -e "at\$cellinfo3G=1\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep CELLINFO3G|awk -F "," '{print $11}'
			if [ "$Brand" = "Qisda" ]; then
            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$cellinfo3G=1\r\n"|grep CELLINFO3G|awk -F "," '{print $11}'
			else
			catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+CREG=2 \r\n"|grep +qwdw
			catty -r 0 -d /dev/$AP_device -b 460800 -w "AT+CREG? \r\n"|grep +CREG:
			fi
            ;;
      band )
            #echo -e "at\$QAB\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^\$QAB|sed -e "s/^\$QAB.*:\"//"|sed -e "s/\"//"
			if [ "$Brand" = "Qisda" ]; then
            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$QAB\r\n"|grep ^\$QAB|sed -e "s/^\$QAB.*:\"//"|sed -e "s/\"//"
			else
			catty -r 0 -d /dev/$AP_device -b 460800 -w "^SYSCFG=2,0,2,4 \r\n"|grep -m 1 MODE
			fi
            ;;
      txrx )
			if [ "$Brand" = "Qisda" ]; then
            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$QTTR=2\r\n"|grep ^\$QTTR|sed -e "s/^\$QTTR://"|awk -F "," '{print $1 "','" $2}'
			else
			catty -r 0 -d /dev/$AP_device -b 460800 -w "^SYSCFG=2,0,2,4 \r\n"|grep -m 1 DSFLOW
			fi
            ;;
#        tx )
            #echo -e "at\$QTTR=2\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^\$QTTR|sed -e "s/^\$QTTR://"|awk -F "," '{print $1}'
#            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$QTTR=2\r\n"|grep ^\$QTTR|sed -e "s/^\$QTTR://"|awk -F "," '{print $1}'
#            ;;
#        rx )
            #echo -e "at\$QTTR=2\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep ^\$QTTR|awk -F "," '{print $2}'
#            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$QTTR=2\r\n"|grep ^\$QTTR|awk -F "," '{print $2}'
#            ;;
      #get Ec/Io and RSCP
  eciorscp )
            #echo -e "at\$cellinfo3G=1\r\n">/dev/$AP_device|head -n 4 /dev/$AP_device|grep CELLINFO3G|awk -F "," '{print $11}'
            catty -r 0 -d /dev/$AP_device -b 460800 -w "at\$cellinfo3G=2\r\n"|grep CELLINFO3G|awk -F "," '{print $3 "','" $4}'
esac
